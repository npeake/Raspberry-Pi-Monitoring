#This file reads DHT sensor temp and humidity and prints the reading to LCD screen
import requests
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import Adafruit_DHT


#define DHT sensor variables
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 9

#LCD screen pin setup
lcd_rs = digitalio.DigitalInOut(board.D27)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D4)
lcd_d5 = digitalio.DigitalInOut(board.D3)
lcd_d6 = digitalio.DigitalInOut(board.D2)
lcd_d7 = digitalio.DigitalInOut(board.D14)

#Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

#LCD initialization
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

#clear any corrupted text first
lcd.clear()

#test
lcd.message = "      Hello     \n      World!    "

#delay to allow function on startup
time.sleep(4.0)

while True:

	for i in range(10):
		#measure and adjust temp/humidity
		humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
		humidity = humidity*.9 #correction factor

		#Print measurement to LCD screen
		lcd.message = " Temp = {0:0.1f}*C\nHumidity = {1:0.1f}%".format(temperature, humidity)
#		lcd.message = "  Temp  = {0:0.1f}*C\nHumidity = {1:0.1f}%".format(temperature, humidity)

		i=i+1
		time.sleep(2)
	lcd.clear()
