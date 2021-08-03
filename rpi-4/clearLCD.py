#this function clears the LCD screen of any unwanted characters

#This file utilizes the MCP3008 ADC chip to read out resistance using a voltage divider network
import math
import sys
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

#Rpi pin setup
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
