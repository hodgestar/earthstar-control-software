#!/bin/sh

while true; do
  sudo /home/pi/earthstar-control-software/led_driver/main \
    >> /home/pi/led-driver.log
done
