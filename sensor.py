#######################################################################################################################

# Project:          Weather Station Project
# File:             sensor.py
#
# Author:           Ho Wun Ng
# Purpose:          Create the general Sensor class
# Description:      Create a Sensor class that stores the name of the sensor. This class should be the base class for all
#                   sensors and the method should be overrode.
# Date last edited: 2023/12/4

#######################################################################################################################

# Classes
class Sensor:
	'''Create a base class for all type of sensor.'''
	def __init__(self,name):
		'''
		Constructor method for the Sensor Class
		Args: Name of the sensor (str)
		'''
		# Sensor name
		self.name = name
	
	# Read sensor data
	def read_sensor_data():
		'''Create a method for sensor subclass to override, raise if this method is called here.'''
		raise Exception("The read_sensor_data method should be overridden by subclasses.")

################## End of Code ########################################################################################





