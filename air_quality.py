#######################################################################################################################

# Project: Weather Station Project
# File: air_quality

# Author: Parmeet Brar
# Purpose: To measure air quality using Adafruit Industries 3199 sensor       
# Description: This script reads the analog voltage off of the output pin of the sensor and converts it to ppm 
#              values for each gas. It then prints the ppm values for each gas to the console.
# Date last edited: 

#######################################################################################################################

# Imports
import time
import board
import busio
import adafruit_mics5524

# Functions 

# Preprocess Definitions

# Classes

# Code

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_mics5524.MICS5524(i2c)

while True:
    print("CO: ", sensor.CO)
    print("Ammonia: ", sensor.nh3)
    print("Ethanol: ", sensor.c2h5oh)
    print("H2: ", sensor.h2)
    print("Methane / Propane / Iso-Butane: ", sensor.c3h8)

    time.sleep(1)


################## End of Code ########################################################################################