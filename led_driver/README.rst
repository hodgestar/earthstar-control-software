Earthstar Driver Software
==========================

Driver software for the Earthstar LED array.

It requires the Earthstar Control software to display anything, as it
has no "patterns" of its own. It listens to the Control software using
ZeroMQ.

Instructions
------------

Requirements: Requires a great WS281X LED driver package, rpi_ws281x
(https://github.com/jgarff/rpi_ws281x) to be cloned into the working 
directory.
* cd led_driver
* clone https://github.com/jgarff/rpi_ws281x

Build: Just run:
* make

Run: a Raspberry Pi requires super user access to use some io, so run
with:
* sudo ./main

Stop: CTRL-c will exit as required
