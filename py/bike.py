#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from adafruit_motorkit import MotorKit

kit = MotorKit()

for i in range(100):
    kit.stepper2.onestep()
