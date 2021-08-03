This directory contains files unique to raspberry pi 3. The job of this pi is to monitor temperature and humidity during thermal cycling or high voltage testing. It can then record this data locally to a CSV file, upload the data to Grafana, display data on the LCD screen attached by flex cable, or all of the above. The LCD files are the mainly unique part of this directory due to the LCD pinouts made using the attached flex. All files can be run headless (no monitor attached), making the pi flexible on where it's placed for monitoring temp/humidity during tests. LCD readout and Grafana sending are currently set to run on startup to allow monitoring once the pi is plugged in at the desired area. A list of the files and their descriptions is included below:

LCDtemp3.py --- reads temp and humidity from DHT 22 sensor and prints to attached LCD screen
                -LCD pinout different from other pi's, requiring a seperate file denoted 3 for rpi-3
                -currently set to refresh every 2 seconds, easily modified
                    -DHT sensor doesn't handle refresh quicker than 1.5 seconds well

LCD.service --- service file to start LCDtemp3.py on startup
                -may need to update reference to LCDtemp3.py file depending on where the repository is installed
                    -reference the file from pi home : "/home/pi/{...where rpi-monitor is installed}/rpi-3/LCDtemp3.py"
                    -copy this change to systemd with "sudo cp LCD.service /etc/systemd/system/"

tempsend22.py --- reads temp and humidity of the DHT 22 sensor
                    -sends this data to Grafana periodically
                    -records data to a CSV file locally on the SD card
                        -this portion of code is commented out by default, uncomment it to store specific test points during thermal cycling or testing to be monitored

temp.service --- launches tempsend22.py on startup
                    -may need to update reference to tempsend22.py file depending on where the repository is installed
                        -reference the file from pi home : "/home/pi/{...where rpi-monitor is installed}/rpi-3/tempsend22.py"
                        -copy this change to systemd with "sudo cp temp.service /etc/systemd/system/"
