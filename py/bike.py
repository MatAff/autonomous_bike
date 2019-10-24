#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fps import FPS
from stepper import BigBoy
from imu import IMU

class Bike():
	def __init__(self):
		self.mtr = BigBoy()
		self.imu = IMU()
		self.fps = FPS(1.0)

		self.steps = 4
		self.pos = 0
		self.threshold = 0.2

	def balance(self):
		x, y, z = bike.imu.get_accelerometer()

		if y < -self.threshold:
			self.mtr.turn_right(self.steps)
		elif y > self.threshold:
			self.mtr.turn_left(self.steps)
		elif self.mtr.pos > 0:
			self.mtr.turn_left(self.steps)
		elif self.mtr.pos < 0:
			self.mtr.turn_right(self.steps)
		else:
			self.mtr.release()

		#print('position', self.mtr.pos)

	def updateFPS(self):
		self.fps.update(verbose=True)

	def cleanup(self):
		print('cleanup')
		self.mtr.release()

bike = Bike()

try:
	while 1:
		bike.updateFPS()
		bike.balance()

except KeyboardInterrupt:
	print('KeyboardInterrupt detected')
finally:
	bike.cleanup()


