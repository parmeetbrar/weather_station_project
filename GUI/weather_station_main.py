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
import GUI
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
    GUI.temp_outdoor = random.randrange(-10, 40)
    GUI.temp_indoor = random.randrange(-10, 40)
    GUI.humidity = 1
    GUI.wind_speed = 1
    GUI.pressure_outdoor = 1
    GUI.refresh_time = 5000
    app = GUI.ClimateControlGUI()
    app.self_update()
    app.refresh_time_var.set(f"{GUI.refresh_time} s")
    app.update_indoor_temperature(GUI.temp_indoor)
    app.run()

def update_data():
    while True:
        GUI.temp_outdoor = random.randrange(-10, 40)
        GUI.temp_indoor = random.randrange(-10, 40)
        GUI.humidity = 1
        GUI.wind_speed = 1
        GUI.pressure_outdoor = 1
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