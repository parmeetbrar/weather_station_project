#######################################################################################################################

# Project: Weather Station Project
# File: Anemometer.py

# Author: Parmeet Brar
# Purpose: This code is for reading wind speed using an anemometer   
# Description: The code takes input from a reed switch which is implimneted as a button and outputs the wind speed
#              in km/h
# Date last edited: 2023-12-2

#######################################################################################################################

# Imports
from gpiozero import Button
import RPi.GPIO as GPIO
import time
import math

# Global variables

radius_cm = 5.0 # Depends on radius of rotating magnet
rotation_count = 0
wind_interval = 5  # How often to report speed
reed_switch_pin = 17  # GPIO pin number for the reed switch

# Functions 

def spin(pin):
    '''Purpose: Increment the global variable wind_count. 
    '''
    global rotation_count
    rotation_count += 1

def calculate_speed(rotations, time_sec):
    '''Purpose: Calculate and return the speed based on wind_count, radius, and time.
       Arguments: time_sec (float)
       Return: speed (float)
    '''
    circumference_cm = (2 * math.pi) * radius_cm
    dist_cm = circumference_cm * rotations
    speed = dist_cm / time_sec
    speed = speed * 0.036
    return speed

# Main Code
def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(reed_switch_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the GPIO pin for the reed switch
    GPIO.add_event_detect(reed_switch_pin, GPIO.FALLING, callback=spin, bouncetime=500)

    try:
        while True:
            current_rotations = rotation_count  # Save the current rotation count
            time.sleep(wind_interval) # Wait for the next interval 
            rotations_in_interval = rotation_count - current_rotations  # Calculate rotations in the interval
            wind_speed = calculate_speed(rotations_in_interval, wind_interval)
            print(wind_speed, "km/h")
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

################## End of Code ########################################################################################
