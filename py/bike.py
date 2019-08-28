#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adafruit_motorkit import MotorKit
import time

kit = MotorKit()

t0 = time.time()
for i in range(155):
    kit.stepper1.onestep(direction=1, style=2)
time.sleep(1)
for i in range(155):
    kit.stepper1.onestep(direction=0, style=2)
t1 = time.time()
print(t1 - t0)
kit.stepper1.release()
