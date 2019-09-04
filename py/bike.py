#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from adafruit_motorkit import MotorKit
import board
import busio
import adafruit_bno055

class IMU():
	def __init__(self):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_bno055.BNO055(self.i2c)
		self.failed = False

	def get_accelerometer(self):
		try:
			if self.failed:
				self.sensor = adafruit_bno055.BNO055(self.i2c)
				self.failed = False
			return self.sensor.accelerometer
		except Exception as e:
			print(e)
			if not self.failed:
				self.failed = True
			return 0,0,0

kit = MotorKit()
sensor = IMU()

steps = 10
threshold = 4

try:
	while 1:
		x, y, z = sensor.get_accelerometer()
		if y > threshold:
			print('turning right')
			for i in range(steps):
			    kit.stepper1.onestep(direction=0, style=2)
		elif y < -threshold:
			print('turning left')
			for i in range(steps):
			    kit.stepper1.onestep(direction=1, style=2)
		else:
			kit.stepper1.release()

except KeyboardInterrupt:
	kit.stepper1.release()
