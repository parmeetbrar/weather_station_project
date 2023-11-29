#######################################################################################################################

# Project: Weather Station Project
# File: 

# Author: Parmeet Brar
# Purpose: This code is for reading wind speed using an anemometer   
# Description: The code takes input from a reed switch which is implimneted as a button and outputs the wind speed
#              in km/h
# Date last edited: 2023-11-29

#######################################################################################################################

# Imports
from gpiozero import Button
import math
import time


# Global variables
wind_count = 0

# This may change after Anemometer is designed 
radius_cm = 5.0

wind_interval = 5 # How often to report speed
wind_speed_sensor = Button(5) # GPIO pin number 5


# Functions 

def spin():
    '''Purpose: Increment the global variable wind_count and print a message. 
    '''
    global wind_count
    wind_count = wind_count + 1
    print("spin" + str(wind_count))

def calaculate_speed(time_sec):
    '''Purpose: Calculate and return the speed based on wind_count, radius, and time.
       Arguments: time_sec (float)
       Return: speed (float)
    '''
    global wind_count
    circumference_cm = (2*math.pi)*radius_cm
    rotations = wind_count

    dist_cm = circumference_cm*rotations
    speed = dist_cm/time_sec
    return speed

# Main Code

def main():
    wind_speed_sensor = Button(5)
    wind_speed_sensor.when_pressed = spin

    # loop to meaure wind speed
    while True:
        wind_count = 0
        time.sleep(wind_interval)
        print(calaculate_speed(wind_interval), "km/h") # check units 

if __name__ == "__main__":
    main()


################## End of Code ########################################################################################