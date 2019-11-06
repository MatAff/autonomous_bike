#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import traceback

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
		self.tilt_constant = -25.0
 
	def balance(self):
		x, y, self.tilt = self.imu.get_acceleration()
		self.goal = int(self.tilt_constant * self.tilt)
		self.response = 'Goal: ' + str(self.goal)
		self.try_step(self.goal - self.pos)
		time.sleep(0.005)

	def balance_initial(self):
		x, y, self.tilt = self.imu.get_acceleration()

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
		running = True
		bike = Bike()
		display = SimpleDisplay()

		display.add(Text(value="Bike Control v1", x=0, y=0))
		display.add(VarNumber(name="motor-pos", prefix=True, y=2, round=2))
		display.add(Text(name="response", y=4))
		display.add(VarNumber(name="tilt", prefix=True, y=6, round=2))
		display.add(VarBar(name="tilt", var_min=-4, var_max=4, length=41, y=7))
		display.add(VarNumber(name="x", prefix=True, y=9, round=2))
		display.add(VarBar(name="x", var_min=-10, var_max=10, length=41, y=10))
		display.add(VarNumber(name="y", prefix=True, y=12, round=2))
		display.add(VarBar(name="y", var_min=-10, var_max=10, length=41, y=13))
		display.add(VarNumber(name="z", prefix=True, y=15, round=2))
		display.add(VarBar(name="z", var_min=-10, var_max=10, length=41, y=16))
		display.add(VarNumber(name="g", prefix=True, y=18, round=2))

		while running:
			# bike.updateFPS()
			#bike.balance_initial()
			bike.balance()
			x, y, z = bike.imu.get_acceleration()
			g = (x**2 + y**2 + z**2) ** 0.5
			running = display.update({
				"tilt": {"value": bike.tilt},
				"response": {"value": bike.response + 10 * ' '},
				"motor-pos": {"value": bike.pos},
				"x": {"value": x},
				"y": {"value": y},
				"z": {"value": z},
				"g": {"value": g},
			})

	except KeyboardInterrupt:
		display.cleanup()
		print('KeyboardInterrupt detected')
	except Exception as e:
		display.cleanup()
		traceback.print_exc()
	finally:
		display.cleanup()
		bike.cleanup()
