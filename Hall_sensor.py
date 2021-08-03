# This scripts interfaces with a Hall Effect sensor to sense the presence of a magnetic field, whose voltage is then displayed on an LCD screen
# It uses the MCP3008 ADC chip to read the analog output voltage of the DRV5056A4QLPG Hall Effect sensor

import math
import sys
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 5
MISO = 6      #Dout
MOSI = 13     #Din
CS   = 19

# Initialize MCP ADC chip
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Define function to tell if a box/door with the sensor equipped is open or closed
# Threshold limit can be adjusted if the sensor is too weak or sensitive
def lidsense(V, limit=1.0):
    return 'Open' if V < limit else 'Closed'

# Rpi pin setup for LCD
lcd_rs = digitalio.DigitalInOut(board.D25)
lcd_en = digitalio.DigitalInOut(board.D24)
lcd_d4 = digitalio.DigitalInOut(board.D23)
lcd_d5 = digitalio.DigitalInOut(board.D18)
lcd_d6 = digitalio.DigitalInOut(board.D15)
lcd_d7 = digitalio.DigitalInOut(board.D14)

# Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

# Initialize LCD
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Clear LCD of any risidual text from before
lcd.clear()

while True:
    for i in range(20):
        # The read_adc function will get the value of the specified channel (0-7)
        voltage =  mcp.read_adc(7)*(3.3/1023)
        voltage = round(voltage, 6)

        message = "V = {0:0.3f} Volts\n{1:^16s}".format(voltage, lidsense(voltage))
        # Print voltage and open/closed to the LCD screen
        lcd.message = message
        print(message)

        # Option to print voltage into command line if running by command line execution
     #   print(voltage, 'Volts')
        # Pause for a second
        time.sleep(.5)
    lcd.clear()   #clear away any LCD text corruptions
