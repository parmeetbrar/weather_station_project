#######################################################################################################################

# Project:          Weather Station Project
# File:             sensor.py
#
# Author:           Ho Wun Ng
# Purpose:          Create the general Sensor class
# Description:      Create a Sensor class that stores the name of the sensor. This class should be the base class for all
#                   sensors and the method should be overrode.
# Date last edited: 4 Dec 2023

#######################################################################################################################

# Classes
class Sensor:
	'''
	Purpose:    Create a base class for all type of sensor
	Arguments:  Name of the sensor
	'''
	def __init__(self,name):
		# Sensor name
		self.name = name
	
	# Read sensor data
	def read_sensor_data(self):
		raise Exception("The read_sensor_data method should be overridden by subclasses.")

################## End of Code ########################################################################################





