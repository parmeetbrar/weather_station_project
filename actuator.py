#######################################################################################################################

# Project:          Weather Station Project
# File:             actuator.py
#
# Author:           Ho Wun Ng
# Purpose:          Create the general Actuator class
# Description:      Create a Actuator class that stores the name of the actuator. This class should be the base class
#                   for all actuators.
# Date last edited: 2023/12/6

#######################################################################################################################

# Classes
class Actuator:
	'''Create a base class for all type of actuator.'''
	def __init__(self,name):
		'''
		Constructor method for the Sensor Class
		Args: Name of the actuator (str)
		'''
		# Actuator name
		self.name = name

################## End of Code ########################################################################################