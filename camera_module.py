#*********************************************************************************************************************************
# Project: Weather Station Project
# 
# Author: Priyanshu Bhateja
# Date Edited: 28-11-2023
# File Name: camera_module.py
# 
# Purpose: A program to allow the camera module to work and take pictures periodically.
#
# Description: The program allows the camera module to operate and take pictures in every one hour, and saves the picture with a 
#              custom time stamp.
#*********************************************************************************************************************************
#*********************************************************************************************************************************
"""
Importing external libraries

"""
import subprocess
import time
import datetime
import threading
import cv2
import numpy as np
import os
import glob

#*********************************************************************************************************************************

class Camera:
    """ 
    Class Definition: Camera
    A class which handles manual and timed camera operations for taking pictures
    """  
    def __init__(self, picture_interval_seconds):
        """
        Contructor (__init__) : Initializes the camera with a specified interval for timed picture taking
        Arguments: self, picture_interval_seconds
        Access: Public      
        """ 
        self.picture_interval_seconds = picture_interval_seconds
        # Flag to control the running of the timed picture-taking thread
        self.running = True

    def take_picture(self):
        """
        Method: take_picture
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

class DayAndNightAnalyzer(Camera):
    
    def analyze_image(self, filename):
        image = cv2.imread(filename)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        avg_brightness = np.mean(gray)
        return avg_brightness


#*********************************************************************************************************************************

# Usage
if __name__ == "__main__":
    camera_analyzer = DayAndNightAnalyzer(picture_interval_seconds=60)
    camera_analyzer.start_timed_pictures()

    time.sleep(10)

    image_files = glob.glob("/home/Pi/Pictures/day_night/*.jpg")
    if image_files:
        latest_image = max(image_files, key=os.path.getctime)
        brightness = camera_analyzer.analyze_image(latest_image)

        if brightness > 60:
            print("Day!")
        else:
            print("Night")
    else:
        print("No image found")
    
#*********************************************************************************************************************************