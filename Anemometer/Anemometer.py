#######################################################################################################################

# Project: Weather Station Project
# File: Anemometer.py

# Author: Parmeet Brar
# Purpose: This code is for reading wind speed using an anemometer   
# Description: The code takes input from a reed switch which is implimneted as a button and outputs the wind speed
#              in km/h
# Date last edited: 2023/12/6

#######################################################################################################################

# Imports
import time
import math
import RPi.GPIO as GPIO
# Import the Sensor Class as parent class
from sensor import Sensor

# Global variables
radius_cm = 1.125 # Depends on radius of rotating magnet
wind_interval = 5  # How often to report speed
reed_switch_pin = 17  # GPIO pin number for the reed switch

# Classes
class Anemometer(Sensor):
    '''Anemometer class, child class of Sensor class for reading wind speed using a reed switch'''

    def __init__(self, name, radius_cm, wind_interval, reed_switch_pin):
        '''
        Constructor method for anemometer class 
        Args: name: Name of the sensor (str)
              radius_cm: Radius of rotating magnet in cm (int)
              wind_interval: How often the wind speed should be recorded (int)
              reed_switch_pin: GPIO pin for reed switch input
        '''
        super().__init__(name)
        self.radius_cm = radius_cm
        self.rotation_count = 0
        self.wind_interval = wind_interval
        self.reed_switch_pin = reed_switch_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.reed_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.reed_switch_pin, GPIO.FALLING, callback=self.spin, bouncetime=500)

    def spin(self, channel):
        '''
        Increment the global variable rotation_count when a falling edge is detected on the reed switch.
        Args: channel: GPIO channel (int)
        '''
        self.rotation_count += 1

    def calculate_speed(self, rotations, time_sec):
        '''
        Calculate and return the speed based on wind_count, radius, and time.
        Args: rotations: Number of rotations (int)
              time_sec: Time interval in seconds (float)
        Returns: Wind speed in km/h (float)
        '''
        circumference_cm = (2 * math.pi) * self.radius_cm
        dist_cm = circumference_cm * rotations
        speed = dist_cm / time_sec
        speed = speed * 0.036
        return speed

    def read_sensor_data(self):
        '''
        Get the current wind speed this method overrides the read_sensor_data method from the base class
        Returns: Wind speed in km/h (float)
        '''
        current_rotations = self.rotation_count
        time.sleep(self.wind_interval)
        rotations_in_interval = self.rotation_count - current_rotations
        wind_speed = self.calculate_speed(rotations_in_interval, self.wind_interval)
        return round(wind_speed, 2)

# Functions
def main():
    '''main mathod for testing the sesnor. This will likely not be used in final application'''
    anemometer = Anemometer("Anemometer", radius_cm, wind_interval, reed_switch_pin)
    try:
        while True:
            wind_speed = anemometer.read_sensor_data()
            print(f"Wind Speed: {wind_speed} km/h")
    except KeyboardInterrupt:
        anemometer.cleanup()

if __name__ == "__main__":
    main()

################## End of Code ########################################################################################
