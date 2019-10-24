#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from fps import FPS
from stepper import BigBoy
from imu import IMU

class Bike():
	def __init__(self):
		self.mtr = BigBoy()
		self.imu = IMU()
		self.fps = FPS(1.0)

		self.steps = 5
		self.max_steps = 60
		self.pos = 0
		self.threshold = 1.5

	def balance(self):
		tilt = bike.imu.get_tilt()
		print('tilt', tilt)

		if tilt < -self.threshold:
			print('leaning left')
			self.try_step(self.steps)
		elif tilt > self.threshold:
			print('leaning right')
			self.try_step(-self.steps)
		elif self.pos > 0:
			print('recentering')
			self.try_step(-self.steps)
		elif self.pos < 0:
			print('recentering')
			self.try_step(self.steps)

		print('position', self.mtr.pos)

	def try_step(self, steps):
		if abs(self.pos + steps) <= self.max_steps:
			self.pos += steps
			self.mtr.step(steps)

	def updateFPS(self):
		self.fps.update(verbose=True)

	def cleanup(self):
		print('cleanup')
		self.mtr.cleanup()

bike = Bike()

try:
	while 1:
		bike.updateFPS()
		bike.balance()

#	bike.mtr.step(-500)
#	bike.mtr.step(500)


except KeyboardInterrupt:
	print('KeyboardInterrupt detected')
finally:
	bike.cleanup()


