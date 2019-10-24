#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#from adafruit_motorkit import MotorKit

import time
import RPi.GPIO as GPIO

PIN_PUL = 17
PIN_DIR = 27
PIN_ENA = 22

class BigBoy(object):
    def __init__(self):
        self.pos = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_PUL, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_DIR, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_ENA, GPIO.OUT, GPIO.LOW)

    def step(self, steps):
        if steps > 0 :
            GPIO.output(PIN_DIR, GPIO.HIGH)
        else:
            GPIO.output(PIN_DIR, GPIO.LOW)
        for s in range(abs(steps)):
            GPIO.output(PIN_PUL, GPIO.HIGH)
            time.sleep(0.075)
            GPIO.output(PIN_PUL, GPIO.LOW)
            time.sleep(0.075)

    def release(self):
        GPIO.cleanup()

#class Steering():
#    def __init__(self):
#        self.pos = 0
#        self.kit = MotorKit()
#
#    def turn_left(self, steps):
#        #print('turning left')
#        for s in range(steps):
#            self.kit.stepper1.onestep(direction=1, style=2)
#        self.pos -= steps
#
#    def turn_right(self, steps):
#        #print('turning right')
#        for s in range(steps):
#            self.kit.stepper1.onestep(direction=0, style=2)
#        self.pos += steps
#
#    def release(self):
#        self.kit.stepper1.release()

if __name__ == "__main__":

    mtr = BigBoy()
    mtr.step(1)
    mtr.release()

