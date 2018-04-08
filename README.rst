Earthstar Control Software
==========================

Control software for the Earthstar.

It comes in three parts:

* ``earthstar-api``: The Flask HTTP API and web interface used to generate
  effect events that are sent to the EffectBox.

* ``earthstar-effectbox``: The numpy-based Python application that turns
  effect events into frames to display on the Earthstar.

* ``earthstar-simulator``: The Python application that displays frames if
  you don't have real Earthstar hardware to display them on.

The pieces communicate using ZeroMQ.


Todo
----

* Add all ring joins.
* White LEDs.
* Put candy stripies into an animation.
* Add post effect capping of colour values.
* Add post effect adjusting of relative brightness of LEDs.
* Spherical co-ordinates unit for rendering to a complete virtual sphere.

Implemented ideas
-----------------

* Added post-effect transformation that maps the virtual ring to the physical
  ring and supports: re-ordering the rings, rotating the rings and
  flipping the rings.
* Added worms unit.
* Added spindots unit.
* Implemented swapping between animations.
* Implemented commands.
* Made the number of LEDs per ring more realistic (450).

Discarded ideas
---------------

* Experiment with the Wii controller.

  * See https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/


Effect ideas
------------

* Sparkle (in progress).
* Full sphere pulse.
* Flames from direction.


Quickstart
----------

Install the earthstar control software::

    $ pip install earthstar[simulator]  # not yet available

Or::

    $ pip install -e .[simulator]  # for development

Run the API, EffectBox and simulator::

    $ earthstar-api
    $ earthstar-effectbox
    $ earthstar-simulator

Or run everything together at once::

    $ earthstar-runner
