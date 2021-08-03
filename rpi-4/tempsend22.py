#File to print to LCD and upload to influx DB
import requests
import time
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import Adafruit_DHT


#Define recording function to send to influx DB
def record(data):
  tags = {"project": "pixel_services", "room":"383", "model": "DHT22"}

  data_str = []
  for measurement, value in data.items():
    tag_str = ",".join([f"{k}={v}" for k, v in tags.items()])
    data_str.append(f"{measurement},{tag_str} value={value} {int(time.time())}")

  requests.post("https://itkpix-srv.ucsc.edu/influxdb/write?db=db0&precision=s", data="\n".join(data_str))

#define DHT sensor variables
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 9

##Rpi pin setup
#lcd_rs = digitalio.DigitalInOut(board.D26)
#lcd_en = digitalio.DigitalInOut(board.D19)
#lcd_d4 = digitalio.DigitalInOut(board.D13)
#lcd_d5 = digitalio.DigitalInOut(board.D6)
#lcd_d6 = digitalio.DigitalInOut(board.D5)
#lcd_d7 = digitalio.DigitalInOut(board.D11)
#lcd_backlight = digitalio.DigitalInOut(board.D11)
#
##Define LCD column and row size
#lcd_columns = 16
#lcd_rows = 2
#
##initialize LCD screen with variables
#lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

#start humidity loop and print to LCD
#lcd.message = '     Hello\n     World!'
#time.sleep(3.0)
#lcd.clear()

time.sleep(20)

while True:
	humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

	#lcd.clear()
	if humidity is not None and temperature is not None and humidity <= 100:
		print("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
		#lcd.message = "  Temp  = {0:0.1f}*C\nHumidity = {1:0.1f}%".format(temperature, humidity)
		record({"temperature": temperature, "humidity": humidity})

	else:
		#lcd.clear()
		print("Failed to retrieve data from the humidity sensor :(")
		#lcd.message = "Failed :("
	time.sleep(2)
