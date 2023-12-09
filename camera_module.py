##################################################################################################################################

# Project:      Weather Station Project
# File Name:    camera_module.py

# Author:       Priyanshu Bhateja
# Purpose:      A program to allow the camera module to work and take pictures periodically.
# Description:  The program allows the camera module to operate and take pictures in every one hour, and saves the picture with a 
#               custom time stamp.
# Date Edited:  28-11-2023
##################################################################################################################################

#Imports
import subprocess
import time
import datetime
import threading
import cv2
import numpy as np
import os
import glob
import RPi.GPIO as GPIO

##################################################################################################################################

#Classes
class Camera:
    """    A class which handles manual and timed camera operations for taking pictures """  

    def __init__(self, picture_interval_seconds):
        """
        Contructor : Initializes the camera with a specified interval for timed picture taking
        Arguments: picture_interval_seconds (float)      
        """ 
        self.picture_interval_seconds = picture_interval_seconds

        # Flag to control the running of the timed picture-taking thread
        self.running = True

    def take_picture(self):
        """
        Method to take a picture and save it with a timestamp
        Arguments: self
        Access: Public
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"/home/Pi/Pictures/day_night/image_{timestamp}.jpg"
        command = f"libcamera-still -o {filename}"
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Picture Taken: {filename}")
        except subprocess.CalledProcessError:
            print("Failed to take picture.")

    def timed_picture_taking(self):
        """
        Method: timed_picture_taking
        Continuously takes pictures at set intervals
        Arguments: self
        Access: Public
        """
        try:
            while self.running:
                self.take_picture()
                time.sleep(self.picture_interval_seconds)
        except KeyboardInterrupt:
            print("Timed picture taking stopped.")

    def start_timed_pictures(self):
        """
        Method: start_timed_pictures
        Start the timed picture taking in another thread
        Arguments: self
        Access: Public
        """        
        self.timed_thread = threading.Thread(target=self.timed_picture_taking)
        self.timed_thread.start()

    def stop_timed_pictures(self):
        """
        Method: stop_timed_pictures
        Stop the timed picture taking in another thread
        Arguments: self
        Access: Public
        """         
        self.running = False
        self.timed_thread.join()

##################################################################################################################################

class DayAndNightAnalyzer(Camera):
    """ 
    Class Definition: DayandNightAnalyzer
    A class which analyzes images and concludes if it's day or night
    """  

    def __init__(self, picture_interval_seconds):
        """
        Constructor: Initializes the picture interval method from the parent class and GPIO setup
        Arguments: self, picture_interval_seconds
        Access: Public
        """          
        super().__init__(picture_interval_seconds)
        self.setup_gpio()

    def setup_gpio(self):
        """
        Method: setup_gpio
        Initializes GPIO pin 17 as output with Pulse Width Modulation (PWM) on RaspberryPi
        Arguments: self
        Access: Public
        """ 
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        self.pwm = GPIO.PWM(17, 100)

        # Start with LED off
        self.pwm.start(0) 
   
    def analyze_image(self, filename):
        """
        Method: analyze_image
        Analyzes brightness of images after converting them to greyscale
        Arguments: self, filename
        Access: Public
        return: Average brightness of the image
        """         
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)

        # LED PWM Configuration
        duty_cycle = max(0, min(100,100 - avg_brightness))
        self.pwm.ChangeDutyCycle(duty_cycle)
        return avg_brightness

    def stop_timed_pictures(self):
        """
        Method: stop_timed_pictures
        Stops the time interval of taking pictures. Stops PWM and cleans GPIO configuration
        Arguments: self
        Access: Public
        """   
        super().stop_timed_pictures
        self.pwm.stop()
        GPIO.cleanup()

##################################################################################################################################

# Usage
if __name__ == "__main__":
    camera_analyzer = DayAndNightAnalyzer(picture_interval_seconds=60)
    camera_analyzer.start_timed_pictures()

    try:
        while True:
            time.sleep(10)
            image_files = glob.glob("/home/Pi/Pictures/day_night/*.jpg")
            if image_files:
                latest_image = max(image_files, key=os.path.getctime)
                brightness = camera_analyzer.analyze_image(latest_image)
                print(f"Brightness: {brightness}")
            else:
                print("No image found")
    except KeyboardInterrupt:
        print("Exit")
        camera_analyzer.stop_timed_pictures()
    
##################################################################################################################################
######################################################## End of code #############################################################