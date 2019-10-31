#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from fps import FPS
from stepper import BigBoy
from imu import IMU
from consoledisplay import SimpleDisplay, Text, VarBar, VarNumber

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
		self.tilt = tilt = bike.imu.get_tilt()

		if tilt < -self.threshold:
			self.response = 'leaning left'
			self.try_step(self.steps)
		elif tilt > self.threshold:
			self.response = 'leaning right'
			self.try_step(-self.steps)
		elif self.pos > 0:
			self.response = 'recentering right'
			self.try_step(-self.steps)
		elif self.pos < 0:
			self.response = 'recentering left'
			self.try_step(self.steps)

	def try_step(self, steps):
		if abs(self.pos + steps) <= self.max_steps:
			self.pos += steps
			self.mtr.step(steps)

	def updateFPS(self):
		self.fps.update(verbose=True)

	def cleanup(self):
		self.mtr.cleanup()

if __name__ == "__main__":
	bike = None
	display = None

	try:
		t0 = time.time()
		running = True
		bike = Bike()
		display = SimpleDisplay()

		display.add(Text(value="Bike Control v1", x=0, y=0))
		display.add(VarNumber(name="motor-pos", prefix=True, y=2, round=2))
		display.add(Text(name="response", y=4))
		display.add(VarNumber(name="tilt", prefix=True, y=6, round=2))
		display.add(VarBar(name="tilt", var_min=-2, var_max=2, length=41, y=7))

		while running:
			# bike.updateFPS()
			bike.balance()
			running = display.update({
				"tilt": {"value": bike.tilt},
				"response": {"value": bike.response},
				"motor-pos": {"value": bike.mtr.pos}
			})

	except KeyboardInterrupt:
		print('KeyboardInterrupt detected')
	except Exception as e:
		print("EXCEPTION", e)
	finally:
		display.cleanup()
		bike.cleanup()