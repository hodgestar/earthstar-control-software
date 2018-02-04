# -*- coding: utf-8 -*-

""" A simulator for the Earthstar.

    It consumes frames from the EffectBox and draws them on the screen.
"""

import faulthandler

import click
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu
import pygame
import zmq

from . import frame_utils


class ExitSimulator(Exception):
    """ Raised when the simulator exits. """


class SimEarthstar(object):
    """ Simulate the Earthstar using pygame. """

    def __init__(self, fps=10, print_fps=False):
        self._display_mode = (
            pygame.HWSURFACE |
            pygame.OPENGL |
            pygame.DOUBLEBUF |
            pygame.RESIZABLE
        )
        self._fps = fps
        self._print_fps = print_fps

    def setup(self):
        faulthandler.enable()
        pygame.init()
        screen_size = (500, 500)

        gl_init(screen_size, self._display_mode)
        self._clock = pygame.time.Clock()
        self._earthstar = Earthstar(300)

    def teardown(self):
        pygame.quit()

    def render(self, frame):
        self._earthstar.update(frame)

    def tick(self):
        earthstar = self._earthstar
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN
                    and event.key == pygame.K_ESCAPE):
                raise ExitSimulator()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    earthstar.rotate_x(5)
                elif event.key == pygame.K_w:
                    earthstar.rotate_x(-5)
                elif event.key == pygame.K_a:
                    earthstar.rotate_y(5)
                elif event.key == pygame.K_s:
                    earthstar.rotate_y(-5)
                elif event.key == pygame.K_z:
                    earthstar.rotate_z(5)
                elif event.key == pygame.K_x:
                    earthstar.rotate_z(-5)
            elif event.type == pygame.VIDEORESIZE:
                screen_size = event.size
                gl_init(screen_size, self._display_mode)
        self._earthstar.display()
        pygame.display.flip()
        self._clock.tick(self._fps)
        if self._print_fps:
            print("FPS: %f" % self._clock.get_fps())


def rotate(v, k, theta):
    """ Rotate v by theta radians about k. """
    ct, st = np.cos(theta), np.sin(theta)
    return v * ct + np.cross(k, v) * st + k * np.dot(k, v) * (1 - ct)


def norm(a, b):
    """ Return a unit normal to a and b. """
    k = np.cross(a, b)
    return k / np.linalg.norm(k)


class Earthstar(object):
    """ Render the Earthstar using OpenGL. """

    MAX_INTENSITY = 1.0

    # colours
    BACKGROUND = [0.5, 0.5, 0.5, 1.0]
    FLOOR = [1., 0.8, 0.8, 0.3]
    VOXEL_OFF = [0.9, 0.9, 0.9, 0.6]
    VOXEL_ON = [0, 0, 1.0, 0.6]

    RING_RADIUS = 100.0
    RING_TILT = np.pi / 6  # 30 degrees
    RING_OFFSET = np.array([1, 1, 1]) * RING_RADIUS * 1.1

    N_RINGS = frame_utils.N_RINGS
    LEDS_PER_RING = frame_utils.LEDS_PER_RING

    TUBE_RADIUS = 5.0
    PANELS_PER_LED = 12

    VERTICES_PER_LED = 2 * 3 * PANELS_PER_LED
    N_COLOURS = N_RINGS * LEDS_PER_RING * VERTICES_PER_LED

    def __init__(self, size):
        self.size = size
        # rotate one degree at the start so rings don't look so
        # lined up
        self.rx = self.ry = self.rz = 1

        self.verts = []
        self.colours = []

        for n, r in [
            [(0, 0, 1), (1, 0, 0)], [(0, 0, -1), (1, 0, 0)],
            [(0, 1, 0), (0, 0, 1)], [(0, -1, 0), (0, 0, 1)],
            [(1, 0, 0), (0, 1, 0)], [(-1, 0, 0), (0, 1, 0)],
        ]:
            n, r = np.array(n), np.array(r)
            k = norm(n, r)
            n = rotate(n, k, self.RING_TILT)
            r = rotate(r, k, self.RING_TILT)
            self.add_ring(k, n, r * self.RING_RADIUS, self.RING_OFFSET)

        self.verts = np.array(self.verts)
        self.colours = np.array(self.colours)

    def _do_rotate(self, cur, delta):
        cur += delta
        cur %= 360
        if cur < 0:
            cur += 360
        return cur

    def rotate_x(self, delta):
        self.rx = self._do_rotate(self.rx, delta)

    def rotate_y(self, delta):
        self.ry = self._do_rotate(self.ry, delta)

    def rotate_z(self, delta):
        self.rz = self._do_rotate(self.rz, delta)

    def add_ring(self, k, n, r, offset):
        """ Add a ring. """
        prev_v, v = None, None
        for theta in np.linspace(0, 2 * np.pi, self.LEDS_PER_RING + 1):
            prev_v = v
            v = rotate(r, n, theta) + offset
            if prev_v is not None:
                self.add_led(k, n, prev_v, v)

    def add_led(self, k, n, prev_v, v):
        """ Add an LED. """
        prev_r, r = None, None
        for theta in np.linspace(0, 2 * np.pi, self.PANELS_PER_LED + 1):
            prev_r = r
            r = rotate(n, k, theta) * self.TUBE_RADIUS
            if prev_r is not None:
                self.add_face([
                    prev_v + prev_r, v + prev_r, v + r, prev_v + r
                ], self.VOXEL_ON)

    def add_face(self, corners, colour):
        """ Add a square face. """
        tl, tr, br, bl = corners

        self.verts.extend([tl, tr, br])
        self.colours.extend([colour] * 3)

        self.verts.extend([br, bl, tl])
        self.colours.extend([colour] * 3)

    def update(self, frame):
        """ Apply frame update.

            A frame should consist of:

            * one row per ring (6 rows)
            * one column per LED (LEDS_PER_RING)
            * three colours per LED (0 - 255)
        """
        assert frame.shape == frame_utils.FRAME_SHAPE
        assert frame.dtype == frame_utils.FRAME_DTYPE
        frame = frame / 255.
        # add opacity of 1.0 to each colour
        colours = np.insert(frame, 3, 1.0, axis=2)
        # flatten before repeat
        colours.shape = (self.N_RINGS * self.LEDS_PER_RING, 4)
        # repeat n vertices per led
        self.colours = np.repeat(colours, self.VERTICES_PER_LED, axis=0)
        # reshape post repeat
        self.colours.shape = (self.N_COLOURS, 4)

    def _render_floor(self):
        right, left = -0.1, 1.0
        floor_corners = [
            [left, left], [left, right], [right, right],
            [right, right], [right, left], [left, left],
        ]
        floor_corners.extend(reversed(floor_corners))
        z = - 0.05 * self.size
        gl.glBegin(gl.GL_TRIANGLES)
        for x, y in floor_corners:
            x = x * self.size
            y = y * self.size
            gl.glVertex3f(x, y, z)
            gl.glColor4f(*self.FLOOR)
        gl.glEnd()

    def display(self):
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glClearColor(*self.BACKGROUND)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        glu.gluLookAt(
            -0.75 * self.size, -0.75 * self.size, 1.75 * self.size,
            0.5 * self.size, 0.5 * self.size, 0.5 * self.size,
            0, 0, 1)

        # We want to rotate about the centre of the cube, so
        # shift, rotate, shift back
        gl.glTranslate(self.size / 2.0, self.size / 2.0, self.size / 2.0)
        gl.glRotatef(self.rx, 1, 0, 0)
        gl.glRotatef(self.ry, 0, 1, 0)
        gl.glRotatef(self.rz, 0, 0, 1)
        gl.glTranslate(-self.size / 2.0, -self.size / 2.0, -self.size / 2.0)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointerf(self.verts)
        gl.glColorPointerf(self.colours)

        gl.glDrawArrays(gl.GL_TRIANGLES, 0, len(self.verts))

        self._render_floor()

        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)


def gl_init(screen_size, display_mode):
    """ Initialize display for OpenGL. """
    pygame.display.set_mode(screen_size, display_mode)

    gl.glEnable(gl.GL_DEPTH_TEST)

    gl.glViewport(0, 0, *screen_size)
    viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    glu.gluPerspective(60.0, float(viewport[2]) / float(viewport[3]),
                       0.1, 2000.0)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()


@click.command(context_settings={"auto_envvar_prefix": "ESC"})
@click.option(
    '--fps', default=10,
    help='Frames per second.')
@click.option(
    '--print-fps/--no-print-fps', default=False,
    help='Turn on or off printing actual frames per second.')
@click.option(
    '--effectbox-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to receive frames from.')
def main(fps, print_fps, effectbox_addr):
    click.echo("Earthstar simulator running.")
    s = SimEarthstar(fps, print_fps)
    s.setup()

    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(effectbox_addr)
    socket.setsockopt_string(zmq.SUBSCRIBE, u"")  # receive everything

    frame = frame_utils.candy_stripes()
    try:
        while True:
            try:
                data = socket.recv(flags=zmq.NOBLOCK)
                frame = np.frombuffer(data, dtype=frame_utils.FRAME_DTYPE)
                frame.shape = frame_utils.FRAME_SHAPE
                s.render(frame)
                click.echo("Frame received.")
            except zmq.ZMQError as err:
                if not err.errno == zmq.EAGAIN:
                    raise
            s.tick()
    except ExitSimulator:
        pass
    finally:
        s.teardown()
    click.echo("Earthstar simulator exited.")
