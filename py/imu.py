#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 20:14:17 2019

@author: ma
"""

import time

import board
import busio
import adafruit_bno055

class IMU():
	def __init__(self):
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_bno055.BNO055(self.i2c)
		#self.last_acceleration = None
		self.last_acceleration = (0,0,0)
		self.bad_readings = 0
		self.failed = False
		self.last_tilt = 0
		self.bogus_readings = 0

	def get_acceleration(self):
		try:
			if self.failed:
				self.sensor = adafruit_bno055.BNO055(self.i2c)
				self.failed = False
			acceleration = self.sensor.acceleration
			if self.sane_reading(acceleration):
				self.last_acceleration = acceleration	
				self.bad_readings = 0
				return acceleration
			else:
				return self.last_acceleration
		except Exception as e:
			print(e)
			if not self.failed:
				self.failed = True
			return 0,0,0

	def sane_reading(self, acceleration):
		x, y, z = acceleration
		for i, value in enumerate([x, y, z]):
			if abs(value) > 300:
				self.bad_readings += 1
				return False
			#if self.last_acceleration is not None:
			#	if abs(value - self.last_acceleration[i]) > 1:
			#		return False
		return True

if __name__ == "__main__":
	imu = IMU()
	try:
		while 1:
			#print("Accleration : x = {:3.3f} y = {:3.3f} z = {:3.3f}".format(*imu.get_acceleration()))
			print(imu.get_tilt())
			time.sleep(1/30)
	except Exception as e:
		print(e)
