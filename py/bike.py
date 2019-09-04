#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from adafruit_motorkit import MotorKit
import board
import busio
import adafruit_bno055

from fps import FPS

class Bike():
	def __init__(self):
		self.mtr = Steering()
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

class Steering():
	def __init__(self):
		self.pos = 0
		self.kit = MotorKit()

	def turn_left(self, steps):
		#print('turning left')
		for s in range(steps):
		    self.kit.stepper1.onestep(direction=1, style=2)
		self.pos -= steps
	
	def turn_right(self, steps):
		#print('turning right')
		for s in range(steps):
		    self.kit.stepper1.onestep(direction=0, style=2)
		self.pos += steps

	def release(self):
		self.kit.stepper1.release()

bike = Bike()

try:
	while 1:
		bike.updateFPS()
		bike.balance()

except KeyboardInterrupt:
	print('KeyboardInterrupt detected')
finally:
	bike.cleanup()
