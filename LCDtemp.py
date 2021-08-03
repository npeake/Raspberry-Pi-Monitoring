#This file reads Sensirion SHT85 sensor temp and humidity and prints the reading to Adafruit LCD screen (PN:181)
import requests
import time
import logging
import sys
import construct
import influxdb

from sensirion_i2c_driver import I2cConnection
from sensirion_i2c_sht.sht3x import Sht3xI2cDevice
from sensirion_i2c_driver.linux_i2c_transceiver import LinuxI2cTransceiver

#packages for displaying on LCD screen
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

#LCD screen pin setup (directly related to how the board is wired and will require updating if wired differently)
lcd_rs = digitalio.DigitalInOut(board.D25)     #pin 4 on LCD
lcd_en = digitalio.DigitalInOut(board.D24)     #pin 6 on LCD
lcd_d4 = digitalio.DigitalInOut(board.D23)     #pin 11 on LCD
lcd_d5 = digitalio.DigitalInOut(board.D18)     #pin 12 on LCD
lcd_d6 = digitalio.DigitalInOut(board.D15)     #pin 13 on LCD
lcd_d7 = digitalio.DigitalInOut(board.D14)     #pin 14 on LCD

#Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

#LCD initialization
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

#clear any corrupted text first
lcd.clear()

#test
#lcd.message = "      Hello     \n      World!    "

#delay to allow function on startup
time.sleep(4.0)

#initialize SHT variables
#change i2c-1 portion to change the reading to a different i2c channel
sht3x = Sht3xI2cDevice(I2cConnection(LinuxI2cTransceiver('/dev/i2c-1')))

while True:

	for i in range(10):
		#take temp/humidity measurements
		sht3x.single_shot_measurement()
		temperature, humidity = sht3x.single_shot_measurement()
		lcd.message = " Temp = {0:0.1f}*C\nHumidity = {1:0.1f}%".format(float(temperature.degrees_celsius), float(humidity.percent_rh))

		i=i+1
		time.sleep(1)
	lcd.clear()


