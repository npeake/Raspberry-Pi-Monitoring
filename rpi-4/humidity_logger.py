import os
import Adafruit_DHT
import time

DHT_Sensor = Adafruit_DHT.DHT22
DHT_Pin = 4

try:
	f = open('/home/pi/humidity.csv', 'a+')
	if os.stat('home/pi/humidity.csv').st_size == 0:
		f.write('Date, Time, Temperature, Humidity\r\n')

except:
	pass

while True:
	humidity, temperature = Adafruit_DHT.read_retry(DHT_Sensor, DHT_Pin)

	if humidity is not None and temperature is not None:
		print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
		f.write('{0}, {1}, {2:0.1f}*C, {3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'),time.strftime('%H:%M'), temperature, humidity))

	else:
		print('Failed to retrieve data from the humidity sensor :(')
	time.sleep(10)

