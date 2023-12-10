#######################################################################################################################

# Project:          Weather Station Project
# File:             weather_station_main.py

# Author:           Parmeet Brar
# Purpose:          Main file to run the Weather Station Project    
# Description:      This file imports and utilizes the sensor classes to read data and update the GUI.
# Date last edited: 2023/12/9

#######################################################################################################################

# Imports
# from sensor import Sensor
# from BME280_sensor import BME280SensorI2C
# from air_quality import AirQualitySensor
# from Anemometer import Anemometer
# from camera_module import Camera
import gui
import threading
import time
import random


# Global variables
# Initialization sensor objects and gui
# bme280_indoor = BME280SensorI2C()
# bme280_outdoor = BME280SensorI2C()
# anemometer = Anemometer("anemometer", 1.125, update_interval, 17)
# air_quality_outdoor =  AirQualitySensor("air_quality_outdoor", 0)
# camera_outdoor = Camera()
# gui = Gui()


def application():
    gui.temp_outdoor = random.randrange(-10, 40)
    gui.temp_indoor = random.randrange(-10, 40)
    gui.humidity = 1
    gui.wind_speed = 1
    gui.pressure_outdoor = 1
    gui.refresh_time=5000
    app = gui.ClimateControlGUI()
    app.self_update()
    app.run()

def update_data():
    while True:
        gui.temp_outdoor = random.randrange(-10, 40)
        gui.temp_indoor = random.randrange(-10, 40)
        gui.humidity = 1
        gui.wind_speed = 1
        gui.pressure_outdoor = 1
        time.sleep(0.5)

def main():
    thread1=threading.Thread(target=application)
    thread2= threading.Thread(target=update_data)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()


################## End of Code ########################################################################################