#######################################################################################################################

# Project:          Weather Station Project
# File:             weather_station_main.py

# Author:           Parmeet Brar
# Purpose:          Main file to run the Weather Station Project    
# Description:      This file imports and utilizes the sensor classes to read data and update the GUI.
# Date last edited: 2023/12/9

#######################################################################################################################

# Imports
from sensor import Sensor
from air_quality import AirQualitySensor
from Anemometer import Anemometer
# from camera_module import Camera
from GUI import GUI
import BME280_sensor
import temperature_control_unit
import threading
import time
import random
import os
import glob
from PIL import Image, ImageTk

from Camera.camera_module_new import DayAndNightAnalyzer, Camera
from Camera.cnn_model_for_pi import RaspiPredictor

# Global variables
air_quality = None
outdoor_temperature = 1
outdoor_humidity = 1
outdoor_pressure = 1
indoor_temperature = None
indoor_humidity = None
wind_speed = 1
sensor_reading_time = 1
sky_conditions = "Unknown"
model_path = './Camera/cloud_image_model.tflite'
image_directory = '/home/Pi/Pictures/day_night/'
picture_interval_seconds = 10

# model_path = '/home/Pi/cloud_image_model.tflite
# picture_interval_seconds = 60
# max_images = 20
# captured_images = []
# camera_analyzer = DayAndNightAnalyzer(picture_interval_seconds)
# predictor = RaspiPredictor(model_path)


# Functions

# Functions
def sensor_data_collection():
    global air_quality,outdoor_temperature,outdoor_humidity,outdoor_pressure
    global indoor_temperature,indoor_humidity
    air_quality_sensor = AirQualitySensor("Air Quality Sensor", 0)
    # 1. Outdoor sensor 2. Indoor sensor
    sensor_vector=BME280_sensor.BME280_init()

    while True:
        # Read air quality sensor data
        air_quality = air_quality_sensor.read_sensor_data()
        # Read outdoor and indoor sensor data
        outdoor_data=sensor_vector[0].read_sensor()
        indoor_data=sensor_vector[1].read_sensor()
        # Update global variables with sensor readings
        outdoor_temperature = round(outdoor_data.temperature,2)
        outdoor_humidity = round(outdoor_data.humidity,2)
        outdoor_pressure = round(outdoor_data.pressure,2)
        indoor_temperature = round(indoor_data.temperature,2)
        indoor_humidity = round(indoor_data.humidity,2)
        # Pause to avoid continous reading
        time.sleep(sensor_reading_time)

def wind_sensor():
    global wind_speed
    radius = 10.125 # Depends on radius of rotating magnet
    wind_interval = 5  # How often to report speed
    reed_switch_pin = 17  # GPIO pin number for the reed switch
    anemometer = Anemometer("Anemometer", radius, wind_interval, reed_switch_pin)
    while True:
        # Read wind speed from anemometer
        wind_speed = anemometer.read_sensor_data()
            
def application():
    '''Initialize the GUI application. This function is for the GUI to run in a thread'''
    GUI.temp_outdoor = 1
    GUI.temp_indoor = 1
    GUI.humidity_outdoor = 1
    GUI.humidity_indoor = 1
    GUI.wind_speed = 1
    GUI.pressure_outdoor = 1
    GUI.refresh_time = 1000
    app = GUI.ClimateControlGUI()
    app.self_update()
    app.refresh_time_var.set(f"{GUI.refresh_time/1000} s")
    app.update_indoor_temperature(GUI.temp_indoor)
    app.run()

def update_data():
    '''Collect sensor data base on GUI refresh rate, send the data to GUI file for GUI update.'''
    while True:
        # Update GUI with sensor data
        GUI.temp_outdoor = outdoor_temperature
        GUI.temp_indoor = indoor_temperature
        GUI.humidity_outdoor = outdoor_humidity
        GUI.humidity_indoor = indoor_humidity
        GUI.wind_speed = wind_speed
        GUI.pressure_outdoor = outdoor_pressure
        GUI.air_quality = air_quality
        GUI.sky_conditions = sky_conditions
        # Pause to match GUI refersh rate
        time.sleep(sensor_reading_time)

def find_latest_file(directory_path):
    ''' 
    Find the latest file in the directory
    Args: director_path (str): Provides a directory path for the image files in jpeg format
    '''
    list_of_files = glob.glob(directory_path + '/*.jpg')  # Adjust the pattern as needed
    if not list_of_files:  # No files found
        return None
    latest_file = max(list_of_files, key=os.path.getmtime)
    return latest_file

def capture_and_predict():
    ''' Captures an image of the sky and predicts the sky conditions based on CNN model '''
    global sky_conditions
    click_picture = Camera(picture_interval_seconds)
    predictor = RaspiPredictor(model_path)

    while True:
        click_picture.take_picture()
        latest_image_path = find_latest_file(image_directory)
        if latest_image_path:
            print(f"Processing image: {latest_image_path}")
            prediction = predictor.predict_image(latest_image_path)
            sky_conditions = prediction
            GUI.image_path = latest_image_path
            print(f"Latest Prediction: {sky_conditions}")
        else:
            print(f"No new Image")
        time.sleep(picture_interval_seconds)

def environment_control():
    fan_pin = 14  # GPIO pin number for fan
    heater_pin = 15  # GPIO pin number for heater
    fan, heater = temperature_control_unit.tcu_init(fan_pin, heater_pin)  # initialize the fan and heater LED
    tcu = temperature_control_unit.TemperatureControlUnit("TCU", heater, fan)  # Create the tcu class
    while True:
        tcu.temperature_control(indoor_temperature,GUI.indoor_desired_temperature,False)
        time.sleep(sensor_reading_time)

def main():
    '''
    Main function for the weather station project. Initialize all the sensors. Start the multithreading process to
    cocurrently update the GUI and Collect data from sensors and cameras
    '''
    # Threads for diffrent functionalities 
    thread_app = threading.Thread(target=application)
    thread_update_data = threading.Thread(target=update_data)
    thread_capture_predict = threading.Thread(target=capture_and_predict)
    thread_sensor_data_collection = threading.Thread(target=sensor_data_collection)
    thread_wind_speed = threading.Thread(target=wind_sensor)
    thread_environment_control = threading.Thread(target = environment_control)
    
    # Start all the threads
    thread_app.start()
    thread_update_data.start()
    thread_capture_predict.start()
    thread_sensor_data_collection.start()
    thread_wind_speed.start()
    thread_environment_control.start()


    # Join all threads
    thread_app.join()
    thread_update_data.join()
    thread_capture_predict.join()
    thread_sensor_data_collection.join()
    thread_wind_speed.join()
    thread_environment_control.join()   

if __name__ == "__main__":
    main()


################## End of Code ########################################################################################
