This repository contains python code created and implemented on Raspberry Pi 4. They include files useful files but not necessary for the current implementation of temperature and humidity monitoring conained within the main rpi-monitor repository. The files included are:

clearLCD.py ---------- This python script clears the LCD screen plugged into rpi 4
                        -It is dependant on the LCD screen pinout of the pi
                        -Can be used with other pi's, but the screen pinout section must be updated

huidity_logger.py ---- This file reads temperature and humidity values from a DHT 22 sensor
                        -It then writes this data to a CSV file (file name and location can be changed)
                        -It also prints these values into the command line if executed there
                        -The code is dependant on the pinout of the DHT, and must be adjusted if a different data pin is used

humprint.py ---------- Similar to the file above, this python script also reads temperature and humidity data from the DHT22 sensor
                        -However, humprint.py then prints these collected values to an LCD screen 
                        -The LCD screen segment is dependant on pinout, so it will need to be updated unless the same pinout is used as rpi4

printtemp.py --------- This file reads temperature and humidity values from an SHT85 sensor
                        -It then prints both these values into the terminal if executed here 

tempsend22.py -------- Similar to humprint.py, this file reads temperature and humidity data from a DHT22 sensor
                        -It also prints these values on the LCD screen attached to rpi4
                        -However, it also uploads this data to an influxDB server

timedisplay.py ------- This file simply displays the current time on the LCD screen attached to rpi4
                        -It can be modified for use with other pi's but the LCD pinout section must be updated accordingly
                        -It makes a good test to ensure a recently set up LCD screen is working properly

time.service  -------- This service file is used to start timedisplay.py on rpi startup or run in the background
                        -The timedisplay.py file is locationally referenced, and will need to be updated if timedisplay.py is anywhere but on the home page
                        -Make sure to reference this new location from home: "/home/pi/..." where ... is the directory location of timedisplay.py from home 
                        -The service file will need to be added to /etc/systemd/system using "sudo cp time.service /etc/systemd/system/" command 
