#!/usr/bin/python3

import board
import busio
import adafruit_bno055
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055(i2c)

failed = False
failedtime = None

while 1:
	#print('Temperature: {} degrees C'.format(sensor.temperature))
	#print('Accelerometer (m/s^2): {}'.format(sensor.accelerometer))
	#print('Magnetometer (microteslas): {}'.format(sensor.magnetometer))
	#print('Gyroscope (deg/sec): {}'.format(sensor.gyroscope))
	#print('Euler angle: {}'.format(sensor.euler))
	#print('Quaternion: {}'.format(sensor.quaternion))
	#print('Linear acceleration (m/s^2): {}'.format(sensor.linear_acceleration))
	#print('Gravity (m/s^2): {}'.format(sensor.gravity))

	try:
		if failed:
			sensor = adafruit_bno055.BNO055(i2c)
			failed = False
		ax, ay, az = sensor.accelerometer
		gx, gy, gz = sensor.gyroscope
		print("Acceleration (m/s^2): x: {:6.2f} y: {:6.2f} z: {:6.2f}  Rotation (deg/sec): x: {:6.2f} y: {:6.2f} z: {:6.2f} ".format(ax, ay, az, gx, gy, gz), end='\r')
	except Exception as e:
		if not failed:
			failed = True
			failedtime = time.time()
		print("Failed state for {:3d} s".format(int(time.time() - failedtime)), e, ' '*50, end='\r')
