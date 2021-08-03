#File to print to LCD and upload to influx DB
import requests
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import Adafruit_DHT
import logging
import influxdb

#Define recording function to send to influx DB
def record(data):
  tags = {"project": "pixel_services", "room":"383", "model": "DHT22"}

  data_str = []
  for measurement, value in data.items():
    tag_str = ",".join([f"{k}={v}" for k, v in tags.items()])
    data_str.append(f"{measurement},{tag_str} value={value} {int(time.time())}")

  requests.post("https://itkpix-srv.ucsc.edu/influxdb/write?db=db0&precision=s", data="\n".join(data_str))


# Define DHT sensor variables
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 9


######## CSV file recording portion, uncomment following lines to record temp and humidity locally in addition to sending to Grafana
######## Additionally need to uncomment several lines in the while loop below
######## Can also comment out influx DB portions and only use CSV recording if ethernet connection is unavailable at testing location
######## Open CSV file to write temp data to

#try:
#	f = open('/home/pi/tempcycle.csv', 'a+')
#	if os.stat('home/pi/tempcycle.csv').st_size == 0:
#		f.write('Date, Time, Temperature, Humidity\r\n')
#
#except:
#	pass


time.sleep(5.0)

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


# Temp and humidity loop

while True:
	# get current time when script is executed
	curr_time = int(time.time())
	success = False

	# Ping DHT sensor for temp and humidity
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

	# Add correction factor to humidity
	humidity = humidity*.9

	# CSV recording bit, uncomment here for local logging
#	f.write('{0}, {1}, {2:0.1f}*C, {3:0.1f}%\r\n'.format(time.strftime('%m/%d/%y'),time.strftime('%H:%M'), temperature, humidity))


	# build an influxDB points dictionary for the values to record
	points = [
	    {
	        "measurement": "humidity",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value= humidity),
	    },
	    {
	        "measurement": "temperature",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value= temperature),
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
		"project": "pixel_services",
		"model": "DHT",
		"room": "383",
	},
	)

	time.sleep(10)
