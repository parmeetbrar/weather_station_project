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
from BME280_sensor import BME280SensorI2C
from air_quality import AirQualitySensor
from Anemometer import Anemometer
# from camera_module import Camera
from GUI import GUI
import threading
import time
import random
import os
import glob
from PIL import Image, ImageTk

from Camera.camera_module import DayAndNightAnalyzer, Camera
from Camera.cnn_model_for_pi import RaspiPredictor

# Global variables
air_quality = None
sensor_reading_time = 1
# Initialization sensor objects and gui
#bme280_indoor = BME280SensorI2C()
#bme280_outdoor = BME280SensorI2C()
#anemometer = Anemometer("anemometer", 1.125, GUI.update_interval, 17)
#air_quality_outdoor =  AirQualitySensor("air_quality_outdoor", 0)
# camera_outdoor = Camera()
# gui = Gui()

# model_path = '/home/Pi/cloud_image_model.tflite
# picture_interval_seconds = 60
# max_images = 20
# captured_images = []
# camera_analyzer = DayAndNightAnalyzer(picture_interval_seconds)
# predictor = RaspiPredictor(model_path)


# Functions
def air_quality_data():
    global air_quality
    air_quality_sensor = AirQualitySensor("Air Quality Sensor", 0)

    while True:
        air_quality = air_quality_sensor.read_sensor_data()
        time.sleep(sensor_reading_time)
def application():
    '''Initialize the GUI application. This function is for the GUI to run in a thread'''
    GUI.temp_outdoor = random.randrange(-10, 40)
    GUI.temp_indoor = random.randrange(-10, 40)
    GUI.humidity = 1
    GUI.wind_speed = 1
    GUI.pressure_outdoor = 1
    GUI.refresh_time = 5000
    app = GUI.ClimateControlGUI()
    app.self_update()
    app.refresh_time_var.set(f"{GUI.refresh_time/1000} s")
    app.update_indoor_temperature(GUI.temp_indoor)
    app.run()

def update_data():
    '''Collect sensor data base on GUI refresh rate, send the data to GUI file for GUI update.'''
    while True:
        GUI.temp_outdoor = random.randrange(-10, 40)
        GUI.temp_indoor = random.randrange(-10, 40)
        GUI.humidity = 1
        GUI.wind_speed = 1
        GUI.pressure_outdoor = 1
        GUI.air_quality = air_quality
        time.sleep(sensor_reading_time)

def camera_and_predictor():

    picture_interval_seconds = 60
    model_path = './Camera/cloud_image_model.tflite'
    camera_analyzer = DayAndNightAnalyzer(picture_interval_seconds)
    predictor = RaspiPredictor(model_path)

    while True:
        camera_analyzer.start_timed_pictures()
        # Wait for a new image to be taken
        time.sleep(picture_interval_seconds)

        #Fetching latest image
        image_files = glob.glob("home/Pi/Pictures/prediction/*.jpg")
        if image_files:
            latest_image = max(image_files, key=os.path.getctime)
            brightness = camera_analyzer.analyze_image(latest_image)
            prediction = predictor.predict_image(latest_image)
            gui_app.update_camera_image_and_predict(latest_image, prediction)
        time.sleep(60)

def main():
    '''
    Main function for the weather station project. Initialize all the sensors. Start the multithreading process to
    cocurrently update the GUI and Collect data from sensors and cameras
    '''
    thread1=threading.Thread(target=application)
    thread2= threading.Thread(target=update_data)
    thread3= threading.Thread(target=camera_and_predictor)
    thread_air_quality = threading.Thread(target=air_quality_data)
    
    thread1.start()
    thread2.start()
    thread3.start()
    thread_air_quality.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread_air_quality.join()

if __name__ == "__main__":
    main()


################## End of Code ########################################################################################