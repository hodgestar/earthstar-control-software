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
