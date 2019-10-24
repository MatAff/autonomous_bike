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
		self.failed = False
		self.last_tilt = 0
		self.bogus_readings = 0

	def get_acceleration(self):
		try:
			if self.failed:
				self.sensor = adafruit_bno055.BNO055(self.i2c)
				self.failed = False
			return self.sensor.acceleration
		except Exception as e:
			print(e)
			if not self.failed:
				self.failed = True
			return 0,0,0


	def get_tilt(self):
		a,b,tilt = self.get_acceleration()
		if abs(tilt) > 300:
			self.bogus_readings += 1
			return self.last_tilt
		self.bogus_readings = 0
		self.last_tilt = tilt
		return tilt

if __name__ == "__main__":
	imu = IMU()
	try:
		while 1:
			#print("Accleration : x = {:3.3f} y = {:3.3f} z = {:3.3f}".format(*imu.get_acceleration()))
			print(imu.get_tilt())
			time.sleep(1/30)
	except Exception as e:
		print(e)
