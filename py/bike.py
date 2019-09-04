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

def turn_left(steps):
	print('turning left')
	for s in range(steps):
	    kit.stepper1.onestep(direction=1, style=2)

def turn_right(steps):
	print('turning right')
	for s in range(steps):
	    kit.stepper1.onestep(direction=0, style=2)

kit = MotorKit()
imu = IMU()

steps = 10
pos = 0
threshold = 1

try:
	while 1:
		x, y, z = imu.get_accelerometer()
		if y < -threshold:
			turn_right(steps)
			pos += steps
		elif y > threshold:
			turn_left(steps)
			pos -= steps
		elif pos > 0:
			turn_left(steps)
			pos -= steps
		elif pos < 0:
			turn_right(steps)
			pos += steps
		else:
			kit.stepper1.release()
		print('position', pos)

except KeyboardInterrupt:
	kit.stepper1.release()
