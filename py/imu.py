#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:14:17 2019

@author: ma
"""

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
