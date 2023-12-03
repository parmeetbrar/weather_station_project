#######################################################################################################################

# Project: Weather Station Project
# File: air_quality

# Author: Parmeet Brar
# Purpose: To measure air quality using Adafruit Industries 3199 sensor       
# Description: This script reads the analog voltage off of the output pin of the sensor and converts it to ppm 
#              values for each gas. It then prints the ppm values for each gas to the console.
# Date last edited: 2023-12-03

#######################################################################################################################

# Imports
import time
from gpiozero import MCP3008

# Functions
def get_air_quality():
    '''Purpose: Get the air quality sensor reading.
        Return: air quality (float)
    '''
    input_channel = 0
    air_quality_sensor = MCP3008(channel=input_channel)
    
    if air_quality_sensor.value > 0.5:
        print("Warning: Low air quality!")
    return "{:.4f}".format(air_quality_sensor.value)

def main():
    while True:
        reading = get_air_quality()
        print("Sensor reading:", reading)
        time.sleep(2)

if __name__ == "__main__":
    main()

################## End of Code ########################################################################################