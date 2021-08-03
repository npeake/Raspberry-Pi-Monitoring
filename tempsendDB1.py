#File to upload SHT85 temp and humidity data to influx DBk
#Used for temp monitoring of SHT85 sensor number 1, uses data on pin 14  and clock on pin 15 (GPIO)

import requests
import time
import logging
import sys
import construct
import influxdb

from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver

time.sleep(2)

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

#initialize SHT variables
sht3x = Sht3xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-3')))


#take temp/humidity measurements

while True:
	# get current time when script is executed
	curr_time = int(time.time())
	success = False

	sht3x.single_shot_measurement()
	temperature, humidity = sht3x.single_shot_measurement()


	# build an influxDB points dictionary for the values to record
	points = [
	    {
	        "measurement": "humidity",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value= humidity.percent_rh),
	    },
	    {
	        "measurement": "temperature",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value= temperature.degrees_celsius),
	    },
	]
	# make an influxdb client
	log.info(f"Writing to influxdb: {points}")
	client = influxdb.InfluxDBClient(
	host="itkpix-srv.ucsc.edu",
	port=443,
	ssl=True,
	verify_ssl=True,
	path="influxdb",
	gzip=True,
	)
	# send the data to influxdb
	success = client.write_points(
	points,
	time_precision="s",
	database="db0",
	tags={
		"project": "pixel_modules",
		"make": "sensirion",
		"model": "SHT85",
		"room": "cleanroom",
		"number":"1",
	},
	)

	time.sleep(5)


