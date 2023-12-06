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
        filename = f"/home/pi/Pictures/data_for_pi/prediction/image_{timestamp}.jpg"
        command = f"raspistill -o {filename}"
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

    def user_input(self):
        """
        Method: user_input
        Handle User Input for manual picture taking or to exit the program
        Arguments: self
        Access: Public
        """           
        print("Type '1' to take a picture immediately, or '0' to stop the program.")
        try:
            while True:
                user_input = input().strip().lower()
                if user_input == '1':
                    self.take_picture()
                elif user_input == '0':
                    self.stop_timed_pictures()
                    break
        except KeyboardInterrupt:
            print("Program stopped")
            self.stop_timed_pictures()

#*********************************************************************************************************************************

# Usage
camera = Camera(picture_interval_seconds=3600)
camera.start_timed_pictures()
camera.user_input()
    
#*********************************************************************************************************************************