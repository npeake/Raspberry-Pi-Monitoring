#File to upload SHT85 temp and humidity data to influx DB
import requests
import time
from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver

#time.sleep(60)

#Define recording function to send to influx DB
def record(data):
  tags = {"project": "pixel_modules", "room": "383", "make": "sensirion", "model": "SHT85"}

  data_str = []
  for measurement, value in data.items():
    tag_str = ",".join([f"{k}={v}" for k, v in tags.items()])
    data_str.append(f"{measurement},{tag_str} value={value} {int(time.time())}")

  requests.post("https://itkpix-srv.ucsc.edu/influxdb/write?db=db0&precision=s", data="\n".join(data_str))

#initialize SHT variables
sht3x = Sht3xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-1')))

#start humidity sensing loop

while True:
	sht3x.single_shot_measurement()
	temperature, humidity = sht3x.single_shot_measurement()

	if humidity is not None and temperature is not None:
		#print(temperature, humidity)
		record({"temperature": temperature.degrees_celsius, "humidity": humidity.percent_rh})

	else:

		print("Failed to retrieve data from the humidity sensor :(")

	time.sleep(2)  #change this value to adjust the frequency of temp/humidity logging
