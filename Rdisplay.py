#This file utilizes the MCP3008 ADC chip to read out resistance using a voltage divider network
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
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

#create voltage divider equation to output resistance given voltage
def Voltdiv(Vin, Vout, R1):
	R2= R1*(Vout/(Vin-Vout))
	return R2*.001

# beta from https://www.mouser.de/datasheet/2/362/ktthermistor-3035.pdf    (beta=3435 for module?)
# beta of 3969 for module test stand sensors from https://digikey.com/en/products/detail/amphenol-advanced-sensors/DC95F103W/241325
def ohm2temp(ohm, beta=3969):
    return (1.0/((1.0/298.15) + (math.log(ohm/10.0)/beta)))-273.15

def kelvin2celsius(temp):
    return temp - 273.15

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

#initialize LCD (and clear any previous text)
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

lcd.clear()

# Main program loop.
while True:
    # The read_adc function will get the value of the specified channel (0-7).
    voltage =  mcp.read_adc(7)*(3.3/1023)
    resistance = Voltdiv(3.30001, voltage, 50800)
    temp=ohm2temp(resistance)
    voltage = round(voltage, 6)
    resistance = round(resistance, 4)
    # Print the ADC values.
    lcd.message = "R = {0:0.3f} kOhms\nT = {1:0.3f} *C".format(resistance, temp)
#    print(voltage, 'Volts')
#    print(resistance, 'Ohms')
    time.sleep(.5)
