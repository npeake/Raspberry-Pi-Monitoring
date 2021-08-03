#This file logs the temperature value measured using a Raspberry Pi along with the MCP3008 ADC chip
#This file utilizes the MCP3008 ADC chip to read out resistance using a voltage divider network
import math
import sys
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import requests
import logging
import construct
import influxdb

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 5
MISO = 6      #Dout
MOSI = 13     #Din
CS   = 19
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#Begin logging connection
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


#Define necessary functions
#Create voltage divider equation to output resistance given voltage
def Voltdiv(Vin, Vout, R1):
	R2= R1*(Vout/(Vin-Vout))
	return R2*.001

# beta from https://www.mouser.de/datasheet/2/362/ktthermistor-3035.pdf
def ohm2temp(ohm, beta=3435):
	return (1.0/((1.0/298.15) + (math.log(ohm/10.0)/beta)))-273.15

#Rpi pin setup
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D18)
lcd_d6 = digitalio.DigitalInOut(board.D15)
lcd_d7 = digitalio.DigitalInOut(board.D14)
#lcd_backlight = digitalio.DigitalInOut(board.D9)

#Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

#initialize LCD
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)
lcd.clear()

while True:
	for i in range(10):    #use this for loop to clear screen every 10th time the temperature is reported to prevent corrupted LCD characters
		# get current time when script is executed
		curr_time = int(time.time())
		success = False
	    # The read_adc function will get the value of the specified channel (0-7).
		voltage = mcp.read_adc(7)*(3.3/1023)
		if voltage==3.3:
			voltage=0
			resistance=NA
			temp=NA
		else:
			voltage=voltage
			resistance = Voltdiv(3.3, voltage, 50800)
			temp=ohm2temp(resistance)
			voltage = round(voltage, 6)
			resistance = round(resistance, 4)
	        # Print the ADC values.
	#       lcd.message = (voltage)
		lcd.message = "R = {0:0.3f} kOhms\nT = {1:0.3f} *C".format(resistance, temp)
	#       print(voltage, 'Volts')
	#       print(resistance, 'Ohms')

		# build an influxDB points dictionary for the values to record
		points = [
		    {
		        "measurement": "resistance",
		        "tags": {},
		        "time": curr_time,
		        "fields": dict(value = resistance),
		    },
		    {
		        "measurement": "temperature",
		        "tags": {},
		        "time": curr_time,
		        "fields": dict(value = temp),
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
		   # "model": "SHT85",
		    "room": "cleanroom",
		},
		)
		i=i+1
		time.sleep(1)
	lcd.clear()
