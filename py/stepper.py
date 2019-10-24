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
        GPIO.setup(PIN_PUL, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_DIR, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(PIN_ENA, GPIO.OUT, initial=GPIO.LOW)

    def step(self, steps, wait=0.001):
        if steps > 0 :
            GPIO.output(PIN_DIR, GPIO.HIGH)
        else:
            GPIO.output(PIN_DIR, GPIO.LOW)
        for s in range(abs(steps)):
            GPIO.output(PIN_PUL, GPIO.HIGH)
            time.sleep(wait/2)
            GPIO.output(PIN_PUL, GPIO.LOW)
            time.sleep(wait/2)

    def release(self):
        GPIO.output(PIN_ENA, GPIO.HIGH)

    def cleanup(self):
        GPIO.output(PIN_ENA, GPIO.HIGH)
        time.sleep(0.5)
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

    import sys
    steps = 5
    wait = 0.001

    try:
        steps = int(sys.argv[1])
        wait = float(sys.argv[2])
    except:
        pass

    mtr = BigBoy()
    print('stepping', steps, 'steps over', wait, 's')
    mtr.step(steps, wait)
    mtr.cleanup()
