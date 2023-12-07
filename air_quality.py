#######################################################################################################################

# Project:          Weather Station Project
# File:             air_quality.py

# Author:           Parmeet Brar
# Purpose:          To measure air quality using Adafruit Industries 3199 sensor       
# Description:      This script reads the analog voltage off of the output pin of the sensor and converts it to ppm 
#                   values for each gas. It then prints the ppm values for each gas to the console.
# Date last edited: 2023/12/7

#######################################################################################################################

# Imports
import time
# Imported ATD convertor class from gpiozero
from gpiozero import MCP3008
# Import the Sensor Class as parent class
from sensor import Sensor

# Classes
class AirQualitySensor(Sensor):
    '''
       AirQualitySensor class, child class of Sensor class for air quality from Mics 5524 sensor and a MCP3008 for the 
       analog to digital conversion
    '''

    def __init__(self, name, input_channel):
        '''
        Constructor method for AirQualitySensor class.
        Args: name: Name of the sensor (str)
                    input_channel: MCP3008 input channel (int)
        '''
        super().__init__(name)
        self.input_channel = input_channel
        self.air_quality_sensor = MCP3008(channel=self.input_channel)

    def read_sensor_data(self):
        '''
        Get the air quality sensor reading.
        Returns: Air quality reading (float) rounded to four decimal places
        '''
        input_channel = 0
        air_quality_sensor = MCP3008(channel=input_channel)
        
        if self.air_quality_sensor.value > 0.5:
            print(f"Warning: Low air quality detected by {self.name} sensor!")
        return round(self.air_quality_sensor.value, 4)

# Functions
def main():
    ''' main mathod for testing the sesnor. This will likely not be used in final application '''
    air_quality_sensor = AirQualitySensor("Air Quality Sensor", 0)

    while True:
        reading = air_quality_sensor.read_sensor_data()
        print(f"{air_quality_sensor.name} Reading: {reading}")
        time.sleep(2)

if __name__ == "__main__":
    main()

################## End of Code ########################################################################################