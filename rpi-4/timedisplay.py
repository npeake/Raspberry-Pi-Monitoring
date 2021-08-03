#File for displaying time on LCD screen
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
#lcd_backlight = digitalio.DigitalInOut(board.D11)

#Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

while True:
	lcd.message = ("Time: %s" %time.strftime("%H:%M:%S"))
#	lcd.cursor_pos = (1,0)
#	lcd.message = ("Date: %s" %time.strftime("%m/%d/%Y"))
#	lcd.message = "Time = {0:0.1f}\nDate = {1:0.1f}%".format(time.strftime("%H:%M:%S"),time.strftime("%m/%d/%Y"))
time.sleep(10.0)
lcd.clear()
