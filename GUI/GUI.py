#######################################################################################################################

# Project: Weather Station Project
# File: Graphical User Interface (GUI)

# Author: Parmeet Brar
# Purpose:       
# Description: 
# Date last edited: 2023/12/12

#######################################################################################################################

# Imports
from tkinter import Tk, Label, Scale, HORIZONTAL, LabelFrame, Button, StringVar, IntVar, Canvas
from PIL import Image, ImageTk
import random
import os

# Global Variables
temp_outdoor = None
temp_indoor = None
humidity = None
wind_speed = None
pressure_outdoor = None
refresh_time = None

# Classes
class ClimateControlGUI():
    ''' 
    ClimateControlGUI class for weather station GUI. This class initializes and manages the graphical user 
    interface for the weather station. 
    '''
    def __init__(self):
        '''Constructor method for ClimateControlGUI class. Initializes the GUI window. '''
        self.root = Tk()
        self.root.title("Climate Control GUI")
        self.root.geometry("800x600") # Initialize the main window size
        self.setup_grid()
        self.setup_variables()
        self.load_images()
        self.create_outdoor_frame()
        self.create_indoor_frame()
        self.create_image_frame()
        self.create_refresh_button()

    def setup_grid(self):
        '''Set up row and column configuration'''
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def setup_variables(self):
         '''Set up global variables and define string variables.'''
        self.base_folder = "C:\\Users\\Parmeet Brar\\Desktop\\MECH 524\\weather_station_project\\GUI"
        self.outdoor_temp_var = StringVar()
        self.outdoor_humidity_var = StringVar()
        self.outdoor_wind_var = StringVar()
        self.outdoor_pressure_var = StringVar()
        self.current_temp_var = StringVar()
        self.desired_temp_var = StringVar()

    def load_images(self):
        '''Load weather condition symbols.'''
        self.weather_images = {
            'cloud': self.load_weather_image('cloud.png'),
            'cold': self.load_weather_image('cold.png'),
            'rain': self.load_weather_image('rain.png'),
            'sunny': self.load_weather_image('sunny.png'),
            'wind': self.load_weather_image('wind.png')
        }

    def create_outdoor_frame(self):
        '''Create outdoor data display frame for GUI'''
        self.outdoor_frame = LabelFrame(self.root, text="OUTDOOR", font=("Helvetica", 16), padx=10, pady=10)
        self.outdoor_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        self.configure_outdoor_frame()
        self.add_outdoor_labels()

    def configure_outdoor_frame(self):
        '''Configure the interior of the frames for resizing'''
        for i in range(5):  # Assuming a maximum of 5 rows in any frame
            self.outdoor_frame.grid_rowconfigure(i, weight=1)
        self.outdoor_frame.grid_columnconfigure(0, weight=1)
        self.outdoor_frame.grid_columnconfigure(1, weight=1)

    def add_outdoor_labels(self):
        ''' Add labels for outdoor temperature, humidity, wind speed, pressure, and weather conditions.'''
        Label(self.outdoor_frame, text="Temperature (°C):").grid(row=0, column=0, sticky="e")
        Label(self.outdoor_frame, textvariable=self.outdoor_temp_var, width=20).grid(row=0, column=1, sticky="w")

        Label(self.outdoor_frame, text="Humidity (%):").grid(row=1, column=0, sticky="e")
        Label(self.outdoor_frame, textvariable=self.outdoor_humidity_var, width=20).grid(row=1, column=1, sticky="w")

        Label(self.outdoor_frame, text="Windspeed (km/h):").grid(row=2, column=0, sticky="e")
        Label(self.outdoor_frame, textvariable=self.outdoor_wind_var, width=20).grid(row=2, column=1, sticky="w")

        Label(self.outdoor_frame, text="Pressure:").grid(row=3, column=0, sticky="e")
        Label(self.outdoor_frame, textvariable=self.outdoor_pressure_var, width=20).grid(row=3, column=1, sticky="w")

        # Weather condition symbol labels
        self.weather_labels = [Label(self.outdoor_frame) for _ in range(3)]
        for i, label in enumerate(self.weather_labels):
            label.grid(row=4, column=i, pady=10, sticky="w")

    def update_indoor_temperature(self,slider_value):
        '''
        Function to update indoor temperature display based on slider value
        Args: slider_value (int), the current value of the temperature adjustment slider.
        '''
        self.desired_temp_var.set(f"{slider_value}°C")

    def create_indoor_frame(self):
        '''Create and setup the indoor frame.'''
        self.indoor_frame = LabelFrame(self.root, text="INDOOR", font=("Helvetica", 16), padx=10, pady=10)
        self.indoor_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.configure_indoor_frame()
        self.add_indoor_components()

    def configure_indoor_frame(self):
        '''Configure the interior of the indoor frame for resizing.'''
        for i in range(8):  # Assuming a maximum of 7 rows in the indoor frame
            self.indoor_frame.grid_rowconfigure(i, weight=1)
        self.indoor_frame.grid_columnconfigure(0, weight=1)
        self.indoor_frame.grid_columnconfigure(1, weight=1)

    def add_indoor_components(self):
        '''Add components for displaying current indoor temperature, adjusting temperature, and desired temperature.'''
        Label(self.indoor_frame, text="Current Temperature:").grid(row=0, column=0, sticky="e")
        current_temp_display = Label(self.indoor_frame, textvariable=self.current_temp_var, width=20)
        current_temp_display.grid(row=0, column=1, sticky="w")

        Label(self.indoor_frame, text="Adjust Temperature:").grid(row=1, column=0, sticky="e")
        Scale(self.indoor_frame, from_=0, to=40, orient=HORIZONTAL, variable=IntVar(),
            command=self.update_indoor_temperature).grid(row=1, column=1, sticky="ew")

        Label(self.indoor_frame, text="Desired Temperature:").grid(row=8, column=0, sticky="e")
        desired_temp_display = Label(self.indoor_frame, textvariable=self.desired_temp_var, width=20)
        desired_temp_display.grid(row=8, column=1, sticky="w")

        # Indoor toggle switches
        toggle_texts = ["Auto", "Heat On", "AC", "Auto Lights", "Energy Saving Mode"]
        for i, text in enumerate(toggle_texts):
            toggle = self.create_toggle(self.indoor_frame, text)
            toggle.grid(row=i+2, column=0, columnspan=2, sticky="ew")

    def create_image_frame(self):
        '''Create and setup the image frame.'''
        self.image_frame = LabelFrame(self.root, text="Camera Image", font=("Helvetica", 16), padx=10, pady=10)
        self.image_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.configure_image_frame()

    def configure_image_frame(self):
        '''Configure the interior of the image frame for resizing.'''
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(0, weight=1)

        # Placeholder for the camera image
        self.camera_canvas = Canvas(self.image_frame, width=760, height=240, bg='light blue')
        self.camera_canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.camera_canvas.create_text(380, 120, text="Camera Image Placeholder", font=("Helvetica", 16))

    def create_refresh_button(self):
        '''Create refresh button'''
        self.refresh_button = Button(self.root, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

    def refresh_data(self):
        '''Method to refresh data using most recent data'''
        self.outdoor_temp_var.set(f"{temp_outdoor}°C")
        self.outdoor_humidity_var.set(f"{humidity}%")
        self.outdoor_wind_var.set(f"{wind_speed} km/h")
        self.outdoor_pressure_var.set(f"{pressure_outdoor} hPa")

        # Update indoor temperature display
        self.current_temp_var.set(f"{temp_indoor}°C")

        # Determine weather conditions based on sensor values
        current_conditions = self.determine_weather_condition(temp_indoor, humidity, wind_speed)

        # Update the weather condition images
        for label, condition in zip(self.weather_labels, current_conditions):
            label.config(image=self.weather_images[condition])
            label.image = self.weather_images[condition]

        # Clear any unused weather labels
        for label in self.weather_labels[len(current_conditions):]:
            label.config(image='')
            label.image = None

    def self_update(self):
        '''This function updates the values on the GUI based on the defined refersh rate.'''
        self.refresh_data()
        self.root.after(refresh_time,self.self_update)

    def load_weather_image(self, filename, size=(50, 50)):
        '''
        Method to load and resize images using PIL
        Args: filename: The name of the image file (str)
              size: The size of which the mage should be resized(tuple). Defaults to (50,50)
        Return: ImageTk.PhotoImage: The resized image as a Tkinter PhotoImage.
        '''
        img = Image.open(os.path.join(self.base_folder, filename))
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def determine_weather_condition(self, temp, humidity, wind_speed):
        '''
        Method to determine weather condition based on sensor values
        Args: temp: The temperature value (float)
              humidity: The humidity value (float)
              wind_speed: The wind speed value 
        Return: conditions: A list of weather conditions determined based on the input sensor values
        '''
        conditions = []
        if temp > 25:
            conditions.append('sunny')
        elif temp < 5:
            conditions.append('cold')
        if humidity > 80:
            conditions.append('rain')
        elif humidity > 70:
            conditions.append('cloud')
        if wind_speed > 25:
            conditions.append('wind')
        return conditions

    def create_toggle(self, parent, text):
        '''
        Create a toggle switch button with specified text.
        Args: parent: The parent frame or widget.
              text: The text to display on the toggle switch (str).
        Returns: toggle: The toggle switch button.
        '''
        var = IntVar(value=0)
        toggle = Label(parent, text=text, relief="raised", width=8, bg="red")
        toggle.var = var

        def on_click(event):
            '''
            Event handler for the toggle switch button click. This method changes the relief and background
            color of the toggle switch button based on its current state.
            Args: event: The click event triggering the method.
            '''
            if toggle.var.get() == 0:
                toggle.config(relief="sunken", bg="green")
                toggle.var.set(1)
            else:
                toggle.config(relief="raised", bg="red")
                toggle.var.set(0)

        toggle.bind("<Button-1>", on_click)
        return toggle

    def run(self):
        ''' Run the main even loop for the GUI'''
        self.root.mainloop()

def main():
    '''
    Main function to instantiate and run the ClimateControlGUI class.
    For testing purposes 
    '''
    app = ClimateControlGUI()
    app.run()

if __name__ == "__main__":
    main()