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

* Add post effect capping of colour values.
* Add a post-effect transformation that maps the virtual ring to the
  physical ring and supports:

  * Re-ordering the rings.
  * Rotating the rings.
  * Reversing the direction of rings.
  * Adjusting relative brightness of RGB LEDs.

* Other approaches to rendering to the ring (effects that take account of
  the rings spatial location).

Implemented ideas
-----------------

* Make the number of LEDs per ring more realistic

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
