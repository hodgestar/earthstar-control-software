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

* Binary clock animation.
* Select final animations.
* Add post effect capping of colour values.
* Spherical co-ordinates unit for rendering to a complete virtual sphere.


Implemented ideas
-----------------

* Make worms ambi-turners.
* And different kinds of worms.
* Add support for reasonable random color generation.
* Option to switch between physical and virtual earthstar settings.
* Fix bug where worms don't cross at zero (probably they are skipping zero).
* Add all ring joins.
* Fixed ordering of colour in simulator.
* Add tests for animations.
* Fixed out-by-one error in segment endpoints when rendering worms.
* Added support for white LEDs in effectbox and simulator doesn't
  break in the presence of the white LEDs.
* Add sparkle animation.
* Added candy stripes animation.
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

* Experiment with the Wii controller (knock-off Wii controller was difficult
  to get working).

  * See https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/wiimote/

* Add post effect adjusting of relative brightness of LEDs (real LEDs seem
  not to need brightness compensation).


Effect ideas
------------

* Full sphere pulse.
* Flames from direction.


Calibration
-----------

1. Set things up, fire up the calibration animation which colours the rings red, green, blue,
   yellow, cyan and magenta, and labels them with a binary grey-white pattern from 0 to 6. It
   also marks the crossing points on each ring.

   $ earthstar-effectbox --transition 1000 --animation calibration

2. Re-order the rings so that they're paired up:

   * (red, green), i.e. (0, 1)
   * (blue, yellow), i.e. (2, 3)
   * (cyan, magenta), i.e. (4, 5)

3. Rotate the ring offsets so that each pair meets at their 0s.

4. Apply manual fiddling to crossing points if needed to get them in the right spots. They
   should be roughly good at the start. Fiddling is just adjusting the points on individual
   rings backwards and forwards some LEDs. Actual crossing mappings should already be taken
   care of.

5. Done!


Quickstart
----------

Install the earthstar control software::

    $ pip install earthstar[simulator,api]  # not yet available

Or::

    $ pip install -e .[simulator,api]  # for development

Run the API, EffectBox and simulator::

    $ earthstar-api
    $ earthstar-effectbox
    $ earthstar-simulator

Or run everything together at once::

    $ earthstar-runner
