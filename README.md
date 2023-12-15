# Weather Station/Smart Home Project

The project utilizes a Raspberry Pi along with some simple sensors to develop a weather station/smart home device. The features of this project present the user with outdoor weather conditions and indoor temperature conditions on a graphical user interface. Additionaly the interface allows the user to control indoor heating, cooling and lighting. The heating, cooling and lighting controls would need to be intigrated with physical control devices in the home this device is being implimented in. The major emphasis is on gathering/analyzing data and control algorithms of indoor conditions.

## Features

1. Data Collection and Logging of the following information:
    - Temperature: Indoor and outdoor
    - Humidity: Indoor and outdoor
    - Pressure: Outdoor
    - Air Quality: Outdoor
    - Wind speed: Outdoor
    - Image: Outdoor
2. Sky Condition Analysis:
Using image processing and a CNN model, analyze sky photos to detect clear, overcast, or wet conditions, as well as day or night.
3. Lighting and Temperature Control:
Using LEDs, simulate dynamic lighting and temperature control depending on user input and sensor data.
4. Graphical User Interface (GUI):
A user-friendly GUI allows the user to access real-time weather data, and control indoor heating, cooling, and lighting
5. Energy-Saving Mode:
Reduce energy usage and enhance environmental sustainability.

## Usage

1. Clone the repository to your RaspberryPi.
    In bash
    git clone [git@github.ubc.ca/MECH-524-101-2023W1/weather_station_project.git](https://github.ubc.ca/MECH-524-101-2023W1/weather_station_project). 
2. Set up the required hardware components as specified in the *documentation* provided.
3. Update your RaspberryPi over an internet connection using the following codes:
                    *sudo apt-get update*
                    *sudo apt-get upgrade*
4. Install the necessary dependencies (list provided in the documentation)
    In case the dependencies fail to install, create a virtual environment using the terminal and install the dependencies with the virtual environment active.
    Create a virtual environment using this code:
                    *python3 -m venv **your_environement_name***
    Activate the environment using this code:
                    *source **your_environment_name**/bin/activate*
5. Run the *main.py* script using RaspberryPi IDE or *main.exe* on the RaspberryPi to start the weather station.

## Hardware

- Raspberry Pi 4B
- BME280 Sensor
- Adafruit MiCS5524 air quality sensor
- Magnetic reed switch and magnet
- Raspberry Pi camera
- Lead lights
- Resistors
- Breadboard

## Documentation

### External Libraries

In order to install external libraries, activate your virtual environment and enter the codes for the libraries listed below:

1. GPIO: Library for General Purpose Input/Output

   ```bash
   sudo apt-get install python3-rpi.gpio
   ```

2. smbus2: Library for interfacing with sensors

   ```bash
   pip3 install smbus2
   ```

3. BME280: Library for using BME280 sensor

   ``` bash
   pip3 install RPi.bme280
   ```

4. Pillow: Image processing library

   ```bash
   pip3 install Pillow
   ```

5. OpenCV (cv2): Library of functions aimed at real-time

   ```bash
   pip3 install opencv-python-headless
   ```

6. Numpy: Library that adds support for multi-dimensional arrays, matrices and high-level mathematical functions

   ```bash
   pip3 install numpy
   ```

7. TensorFlow Lite (TFLite): Deep learning framework for on-device interface

   ```bash
   pip3 install tflite-runtime
   ```

### Imports

1. General imports

   ```python
   import time
   import math
   import numpy as np
   import threading
   import os
   ```

2. Sensor Imports

   Imports used in the specific files that impliment the following sensors

   ```python
   # Camera imports
   import subprocess
   import time
   import datetime
   import cv2
   import glob
   import RPi.GPIO as GPIO
   import tensorflow as tf
   from keras.preprocessing.image import ImageDataGenerator
   from keras.preprocessing import image
   import tflite_runtime.interpreter as tflite
   from PIL import Image
   ```

   ```python
   # Anemometer imports
   import RPi.GPIO as GPIO
   ```

   ```python
   # BME280 sensor imports
   import smbus2
   import bme280
   ```

   ``` python
   #Air Quality sensor imports
   from gpiozero import MCP3008
   ```

   ```python
   # Control simulation imports
   from gpiozero import LED
   ```

3. GUI imports

   ```python

   from tkinter import Tk, Label, Scale, HORIZONTAL, LabelFrame, Button, StringVar, IntVar, Canvas, Toplevel, LEFT
   from PIL import Image, ImageTk
   import random
   import os
   from camera_module_new import Camera, DayAndNightAnalyzer
   from cnn_model_for_pi import RaspiPredictor
   import glob
   ```

## License

This project is licensed under the UBC GitHub License.

## Acknowledgement

- This project utilizes open-source libraries and resources from the community.
- Information on raspberry pi programming and weather monitoring using raspberry pi was used from [raspberrypi.org](https://www.raspberrypi.org/).
- ChatGPT was used for providing coding help during the development process and assisting with debugging

## Authors

1. Parmeet Brar:        Student ID: 20877288
2. Priyanshu Bhateja:   Student ID: 81567786
3. Halvard Ng:          Srudent ID: 41277492