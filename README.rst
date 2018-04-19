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
* Binary clock animation.
* Select final animations.
* Add post effect capping of colour values.
* Spherical co-ordinates unit for rendering to a complete virtual sphere.


Implemented ideas
-----------------

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
