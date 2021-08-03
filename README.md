This repository contains all python code created for use on Raspberry Pi's to read out temperature values from various connectors to monitor the UCSC, ATLAS ITk Pixel module test stand. 

The tempsendDB.py file creates a connection with an SHT85 connector through I2C of the Raspberry Pi. This sensor then monitors the cold plate the module sits on, cooled by a seperate cooling unit. The temperature value is recorded and sent to an influxDB to finally be plotted on Grafana.

The logNTC.py file reads the temperature from the NTC attached to the module and prints this value on an LCD screen in the lab. Reading an NTC requires an analogue signal readout, so we used the MCP3000 ADC chip along with the Raspberry Pi to measure a voltage and convert it to temperature. The file contains several functions using the voltage divider created for measuring the voltage, which converts the measured voltage in the divider into a resistance value. From there, the NTC resistance is converted into a temperature value using another created function. Finally, the temperature value is sent to the influxDB and plotted on Grafana. 

The tempsend.py file sends temperature and humidity values recorded from DHT sensors to the influx database. This file is capable of running on startup from rc.local. It also contains all functionality for saving data to CSV locally on Pi, printing values to terminal, and outputting values to LCD. As is, these properties are commented out by default for most basic temperature sending functionality. 

tempsend2.py sends temperature and humidity values recorded from SHT85 sensors wire to I2C pins to the influx database. It's a barebones version of tempsend.py adapted for SHT85 sensors. However, it can be easily adapted to perform same functions as tempsend.py as well as log temperatures to CSV. 

The notes.txt file contains descriptions for the remianing files in the repository and how to implement them.

The setup.txt file contains all packages necessary to install before using all of the python scripts within this repository. The installation must be done manually after the install but detailed instructions for this process are included there. 
