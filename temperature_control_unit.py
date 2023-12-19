#######################################################################################################################

# Project:          Weather Station Project
# File:             temperature_control_unit.py
#
# Author:           Ho Wun Ng
# Purpose:          Create the temperature control unit, and the state class for the unit
# Description:      Create a TemperatureControlUnit class. The unit will be a state machine where it has three states,
#                   heating cycle, neutral cycle and cooling cycle. Each state has been defined as a subclass of the
#                   state class. Each of them will adjust to turn the fan and heater on and off.
# Date last edited: 2023/12/19

#######################################################################################################################

# Imports
from gpiozero import LED
# Imort the Parent class Actuator for the TemperatureControlUnit class
from actuator import Actuator
import time

# Global Variable
ac_state = False
heater_state = False

# Classes
class TemperatureControlUnit(Actuator):
    '''Main class for the temperature control unit. Contains methods for initialization and switching states and '''
    def __init__(self, name, heater, fan):
        '''
		Constructor of the TemperatureControlUnit class
		Arguments:	Name of the sensor for base class constructor (str)
					heater unit (a LED for demonstration purpose)  (LED class)
					cooler unit (a LED for demonstration purpose)  (LED class)
		'''
        super().__init__(name)
        self.heater = heater
        self.fan = fan
        # Set the states of the unit
        self.state = [CoolingCycle(), NeutralCycle(), HeatingCycle()]
        # Set initial state as neutral
        self.current_state = self.state[1]
        self.current_state.execute(heater, fan)
    
    def temperature_control(self, current_temp, desired_temp, power_saver : bool):
        '''
        Main control of the unit, choose the states based on current temperature and the desired temperature
        '''
        global ac_state, heater_state
        temp_diff = 5 if power_saver else 0 
        
        if current_temp is not None and desired_temp is not None:
            # Cooling State
            if self.current_state is self.state[0]:
                if current_temp < (desired_temp + temp_diff - 1):
                    self.set_to_neutral()
                    ac_state = False

            # Neutral State
            elif self.current_state is self.state[1]:
                    if current_temp > (desired_temp + temp_diff + 3):
                        self.set_to_cool()
                        ac_state = True
                    elif current_temp < (desired_temp - temp_diff - 3):
                        self.set_to_heat()
                        heater_state = True
                    else:
                        pass

            # Heating State
            elif self.current_state is self.state[2]:
                    if current_temp > (desired_temp - temp_diff + 1):
                        self.set_to_neutral()
                        heater_state = False
    
    def set_to_cool(self):
        '''Set unit to cooling state'''
        self.current_state = self.state[0]
        self.current_state.execute(self.heater, self.fan)

    def set_to_neutral(self):
        '''Set unit to neutral state'''
        self.current_state = self.state[1]
        self.current_state.execute(self.heater, self.fan)

    def set_to_heat(self):
        '''Set unit to heating state'''
        self.current_state = self.state[2]
        self.current_state.execute(self.heater, self.fan)
		

class State:
    '''Parent class for the state machine. Contain methods for override in child class'''
    def execute(self):
        pass

class HeatingCycle(State):
    '''Child class for the state machine. Contain methods for heating state operation'''
    def execute(self, heater, fan):
        '''
		Change the state of the machine to heating cycle
		Arguments:	Name of the sensor for base class constructor (str)
					heater unit (a LED for demonstration purpose)  (LED class)
					cooler unit (a LED for demonstration purpose)  (LED class)
		'''
        # Enable heater/LED, disable fan/LED
        heater.on()
        fan.off()

class CoolingCycle(State):
    '''Child class for the state machine. Contain methods for cooling state operation'''
    def execute(self, heater, fan):
        '''
		Change the state of the machine to cooling cycle
		Arguments:	Name of the sensor for base class constructor (str)
					heater unit (a LED for demonstration purpose)  (LED class)
					cooler unit (a LED for demonstration purpose)  (LED class)
		'''
        # Enable fan/LED, disable heater/LED
        heater.off()
        fan.on()

class NeutralCycle(State):
    '''Child class for the state machine. Contain methods for neutral state operation'''
    def execute(self, heater, fan):
        '''
		Change the state of the machine to neutral cycle
		Arguments:	Name of the sensor for base class constructor (str)
					heater unit (a LED for demonstration purpose)  (LED class)
					cooler unit (a LED for demonstration purpose)  (LED class)
		'''
        # disable both fan/LED and heating/LED
        heater.off()
        fan.off()

# Functions
def tcu_init(fan_pin, heater_pin):
    '''
    Initialize the temperature control unit
    Arguments:	heater unit connected pin (a LED for demonstration purpose)  (int)
                cooler unit connected pin (a LED for demonstration purpose)  (int)
    Return:     Fan as a LED class (LED)
                Heater as a LED class (LED)
    '''
    fan = LED(fan_pin)
    heater = LED(heater_pin)
    return(fan, heater)

# For testing purposes
def main():
    '''
    Create a function for testing the temperature control unit, it will initialize the unit, switch to cooling state
    for 1 sec, then 1 sec in neutral state, 1 sec in heating state, and repeat.
    '''
    fan_pin = 14  # GPIO pin number for fan
    heater_pin = 15  # GPIO pin number for heater
    fan, heater = tcu_init(fan_pin, heater_pin)  # initialize the fan and heater LED
    tcu = TemperatureControlUnit("TCU", heater, fan)  # Create the tcu class
    wait_time = 1  # set wait time
    # Test the circuit, turn on cooler for 1 second, then off for 1 second, them heater for 1 second,
    # repeat until program stop
    while True:
        tcu.set_to_cool()
        time.sleep(wait_time)
        tcu.set_to_neutral()
        time.sleep(wait_time)
        tcu.set_to_heat()
        time.sleep(wait_time)
    

if __name__ == '__main__':
	# Start the main function
	main()

################## End of Code ########################################################################################
