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

class MusicalMotor():
    def __init__(self, mtr):
        self.mtr = mtr
        self.basenote = "e"
        self.basefrequency = 1 / 0.0002
        self.baseoctave = 5
        self.noteletters = ["a", "a#", "b", "c", "c#", "d", "d#", "e", "f", "f#", "g", "g#"]
        self.notes = {}
        for octave in range(3,7):
            for note in range(12):
                power = 12 * (octave - self.baseoctave) + note - self.noteletters.index(self.basenote)
                self.notes[str(octave) + self.noteletters[note]] = self.basefrequency * ((2 ** (1/12)) ** power)
    
    def playnote(self, note, notelength, pause):
        print('playing note', note, self.notes[note])
        self.mtr.step(notelength, self.notes[note])
        print('pausing for', pause)
        time.sleep(pause)

    def printnotes(self):
        for k in sorted(self.notes.keys()):
            v = self.notes[k]
            print(k, "\t", round(v, 8))



if __name__ == "__main__":

    import sys
    steps = 5
    wait = 0.01

    try:
        steps = int(sys.argv[1])
        wait = float(sys.argv[2])
    except:
        pass

    mtr = BigBoy()
    #print('stepping', steps, 'steps over', wait, 's')
    #start_time = time.time()
    #mtr.step(steps, wait)
    #print('Elapsed time: ', time.time() - start_time)

    mm = MusicalMotor(mtr)
    mm.printnotes()
    notelength = 400
    song = ["5c", "5c", "5d", "5c", "5f", "5e"]
    for note in song:
        mm.playnote(note, notelength, 0.1)

    mtr.cleanup()
