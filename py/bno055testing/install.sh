#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo pip3 install --upgrade setuptools
pip3 install RPI.GPIO adafruit-blinka adafruit-circuitpython-bno055

echo Should display: /dev/i2c-1  /dev/spidev0.0  /dev/spidev0.1
ls /dev/i2c* /dev/spi*
echo If not, enable I2C and SPI interfaces in raspi-config.
