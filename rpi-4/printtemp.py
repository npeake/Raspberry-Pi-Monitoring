#this code reads SHT85 and prints to terminal

import requests
import time
import logging
import sys
import construct
import influxdb

from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver

#time.sleep(20)

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

## get current time when script is executed
#curr_time = int(time.time())
#success = False

#initialize SHT variables

while True:

		sht3x = Sht3xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-1')))

		#take temp/humidity measurements
		curr_time = int(time.time())
		success = False

		sht3x.single_shot_measurement()
		temperature, humidity = sht3x.single_shot_measurement()

		print(temperature,'-----',humidity)
	#	print(humidity)
		print('-----------------------------------')

		time.sleep(2)
