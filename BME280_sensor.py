#######################################################################################################################

# Project:			Weather Station Project
# File:				BME280_sensor.py
#
# Author:			Ho Wun Ng
# Purpose:			Create the BME280SensorI2C Class, read data from the sensor with I2C connection
# Description:		Initialize the BME280 sensors, create a function for sending sensor humidity,
#					pressure and temperature Data
# Date last edited:	2023/12/5

#######################################################################################################################

# Imports
import time
import smbus2
# BME280 sensor I2C communication module
import bme280
# Import the Sensor Class
from sensor import Sensor

# Classes
class BME280SensorI2C(Sensor):
	'''Create a object for the BME280 sensor with I2C connection'''
	def __init__(self, name, bus, address, com_params):
		'''
		Constructor of the BME280SensorI2C class
		Arguments:	Name of the sensor for base class constructor (str)
					I2C bus number (int)
					I2C address (hex)
					Sensor Compensation parameter for use in bme280 library (params)
		'''
		super().__init__(name)
		self.__bus = bus
		self.__address = address
		self.__com_params = com_params
	
	def get_bus(self):
		'''
		Get the I2C bus
		Return: The sensor I2C bus number (int)
		'''
		return self.__bus
	
	def get_address(self):
		'''
		Get the Sensor I2C Address
		Return: The sensor I2C address (int)
		'''
		return self.__address
	
	def get_params(self):
		'''
		Get the Sensor I2C parameters
		Return: The sensor compensation parameter (params)
		'''
		return self.__com_params
	
	def get_sensor_data(self):
		'''
		Receive data from the BME280 sensor reading, then return the data for temperature, pressure and humidity
		Return:	Temperature reading in °C (float)
				Pressure in hPa(float)
				humidity in %rH (float)
		'''
		data = bme280.sample(self.__bus, self.__address, self.__com_params)
		return (data.temperature, data.pressure, data.humidity)
	
	def read_sensor(self):
		'''
		Receive data from the BME280 sensor, the return the data as compensated_readings class
		Return: compensated_readings class containing the readings from the sensor, including the sensor id,
				timestamp, temperature, humidity and pressure readings. (compensated_readings)
		'''
		# Storing the sensor readings
		data = bme280.sample(self.__bus, self.__address, self.__com_params)
		return data
	
# Functions
def BME280_init():
	'''
	To initialize the indoor and outdoor sensor and create the BME280Sensor class for each one.
	Return:		A vector with two BME280Sensor class object, one for outdoor and indoor
	'''
	port = 1
	# outdoor sensor
	outdoor_bme280_address = 0x76
	# indoor sensor
	indoor_bme280_address = 0x77
	# I2C bus on RPi
	bus = smbus2.SMBus(port)
	# Initiating the sensor data parameter
	outdoor_bme280_params = bme280.load_calibration_params(bus, outdoor_bme280_address)
	indoor_bme280_params = bme280.load_calibration_params(bus, indoor_bme280_address)
	# save the two bme280 class
	outdoor_bme280 = BME280SensorI2C("outdoor_bme280",bus, outdoor_bme280_address, outdoor_bme280_params)
	indoor_bme280 = BME280SensorI2C("indoor_bme280",bus, indoor_bme280_address, indoor_bme280_params)
	return (outdoor_bme280, indoor_bme280)

# For testing purposes
def main():
	'''Create a function for testing the BME280 sensor'''
	# 1. Outdoor sensor 2. Indoor sensor
	sensor_vector=BME280_init()
	# Collecting the data from the two sensors repeatedly every 1 second
	while True:
		for i in sensor_vector:
			# Display the data from the bme280 sensor
			data=i.read_sensor()
			print("Sensor Name", i.name)
			print("Sensor ID: ", data.id)
			print("Sensor Time Stamp: ", data.timestamp)
			print("Temperature: ", data.temperature)
			print("Pressure: ", data.pressure)
			print("Humidity: ", data.humidity)
			print("\n Sensor own output:\n",data)
			print('')
		# Wait 1 second before repeat
		time.sleep(1)

if __name__ == '__main__':
	# Start the main function
	main()

################## End of Code ########################################################################################





