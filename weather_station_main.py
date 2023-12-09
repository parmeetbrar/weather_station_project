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
from camera_module import Camera
####IMPORT GUI######



# Global variables
update_interval = 5 # read data every read_intreval

# Initialization sensor objects and gui
bme280_indoor = BME280SensorI2C()
bme280_outdoor = BME280SensorI2C()
anemometer = Anemometer("anemometer", 1.125, update_interval, 17)
air_quality_outdoor =  AirQualitySensor("air_quality_outdoor", 0)
camera_outdoor = Camera()
gui = Gui()


# Functions 
update_gui(temp_outdoor, temp_indoor, humidity_outdoor, air_quality_outdoor, wind_speed_outdoor)

	


# Main Function
def main():
    # initialize GUI
    gui.initialize
    
    while True:
        temp_outdoor
        temp_indoor
        humidity_outdoor
        image_outdoor = camera_outdoor.take_picture
        air_quality= air_quality_outdoor.read_sensor_data
        wind_speed = anemometer.read_sensor_data

        # Update GUI with the sensor data
        gui.update_gui(temp_outdoor, temp_indoor, humidity_outdoor, air_quality, wind_speed)
        time.sleep(update_interval)

if __name__ == "__main__":
    main()


################## End of Code ########################################################################################
