#this code reads NTC resistance from 3 NTCs on breadboard and reports temp to Grafana
import math
import sys
import time
import board
import digitalio
import requests
import logging
import construct
import influxdb
import adafruit_character_lcd.character_lcd as characterlcd

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


#Define necessary functions
#Create voltage divider equation to output resistance given voltage
def Voltdiv(Vin, Vout, R1):
	R2= R1*(Vout/(Vin-Vout))
	return R2*.001

#beta from NTC (Digikey PN 235-1004-ND, Amphenol Thermometrics)
def ohm2temp(ohm, beta=3969):
	return (1.0/((1.0/298.15) + (math.log(ohm/10.0)/beta)))-273.15


# Software SPI configuration:
CLK  = 5
MISO = 6      #Dout
MOSI = 13     #Din
CS   = 19
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)


#Rpi pin setup (may differ depending on board used, currently implemented on rpi4)
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D18)
lcd_d6 = digitalio.DigitalInOut(board.D15)
lcd_d7 = digitalio.DigitalInOut(board.D14)

#Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

#initialize LCD
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.clear()


#Begin logging connection
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


while True:
	#-------------------------------------------------------------------------------------------------------

	#grab values for NTC number 1

	# get current time when script is executed
	curr_time = int(time.time())
	success = False
    # The read_adc function will get the value of the specified channel (0-7).
	voltage1 = mcp.read_adc(7)*(3.3/1023)
	if voltage1==3.3:
		resistance1 = float(0.000)
		temp1 = float(0.000)
	else:
		voltage1 = voltage1
		resistance1 = Voltdiv(3.3, voltage1, 50800)
		temp1 = ohm2temp(resistance1)

	# build an influxDB points dictionary for the values to record
	points = [
	    {
	        "measurement": "resistance",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value = resistance1),
	    },
	    {
	        "measurement": "temperature",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value = temp1),
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
	    "make": "NTC",
	    "number": "1",
	    "room": "cleanroom",
	},
	)


	#-------------------------------------------------------------------------------------------------------

	#grab values for NTC number 2

	# get current time when script is executed
	curr_time = int(time.time())
	success = False
    # The read_adc function will get the value of the specified channel (0-7).
	voltage2 = mcp.read_adc(6)*(3.3/1023)
	if voltage2==3.3:
		resistance2 = float(0.0)
		temp2 = float(0.0)
	else:
		voltage2 = voltage2
		resistance2 = Voltdiv(3.3, voltage2, 49810)
		temp2 = ohm2temp(resistance2)

	# build an influxDB points dictionary for the values to record
	points = [
	    {
	        "measurement": "resistance",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value = resistance2),
	    },
	    {
	        "measurement": "temperature",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value = temp2),
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
	    "make": "NTC",
	    "number": "2",
	    "room": "cleanroom",
	},
	)

	#-------------------------------------------------------------------------------------------------------

	#grab values for NTC number 3

	# get current time when script is executed
	curr_time = int(time.time())
	success = False
    # The read_adc function will get the value of the specified channel (0-7).
	voltage3 = mcp.read_adc(5)*(3.3/1023)
	if voltage3==3.3:
		resistance3 = float(0.0)
		temp3 = float(0.0)
	else:
		voltage3 = voltage3
		resistance3 = Voltdiv(3.3, voltage3, 51480)-.188
		temp3 = ohm2temp(resistance3)

	# build an influxDB points dictionary for the values to record
	points = [
	    {
	        "measurement": "resistance",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value = resistance3),
	    },
	    {
	        "measurement": "temperature",
	        "tags": {},
	        "time": curr_time,
	        "fields": dict(value = temp3),
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
	    "make": "NTC",
	    "number": "3",
	    "room": "cleanroom",
	},
	)


	#-------------------------------------------------------------------------------------------------------
	#print NTC 2 and NTC 3 temperaturess on the  LCD screen

	lcd.clear()

	lcd.message = "Th = {0:0.3f} *C\nTc = {1:0.3f} *C".format(temp2, temp3)

	time.sleep(4)  #wait to sample temp again

