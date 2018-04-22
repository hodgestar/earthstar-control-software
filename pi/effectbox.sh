#!/bin/sh

while true; do
  /home/pi/earthstar-control-software/ve/bin/earthstar-effectbox \
    --fps 17 \
    --transition 60 \
    --etype earthstar \
    >> /home/pi/effectbox.log
done
