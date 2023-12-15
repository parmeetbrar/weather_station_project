#######################################################################################################################

# Project: Weather Station Project
# File: Graphical User Interface (GUI)

# Author: Parmeet Brar
# Purpose:       
# Description: 
# Date last edited: 2023/12/12

#######################################################################################################################

# Imports
from tkinter import Tk, Label, Scale, HORIZONTAL, LabelFrame, Button, StringVar, IntVar, Canvas, Toplevel, LEFT
from PIL import Image, ImageTk
import random
import os

# Global Variables
temp_outdoor = None
temp_indoor = None
humidity = None
wind_speed = None
air_quality = None
pressure_outdoor = None
refresh_time = None

# Threshholds
EXTREME_TEMPERATURE_THRESHOLD = (0, 35)  # Example range in Celsius
EXTREME_HUMIDITY_THRESHOLD = (20, 80)  # Example range in percentage
EXTREME_PRESSURE_THRESHOLD = (980, 1020)  # Example range in hPa

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
        self.create_refresh_rate_frame()
        self.create_refresh_display()
        self.create_refresh_button_up()
        self.create_refresh_button_down()
        self.create_refresh_button()

    def setup_grid(self):
        '''Set up row and column configuration'''
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

    def setup_variables(self):
        '''Set up global variables and define string variables.'''
        self.base_folder = "GUI"
        self.outdoor_temp_var = StringVar()
        self.outdoor_humidity_var = StringVar()
        self.outdoor_wind_var = StringVar()
        self.outdoor_pressure_var = StringVar()
        self.current_temp_var = StringVar()
        self.desired_temp_var = StringVar()
        self.refresh_time_var = StringVar()

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
        for i in range(6):  # Assuming a maximum of 5 rows in any frame
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

        Label(self.outdoor_frame, text="Air Quality:").grid(row=4, column=0, sticky="e")
        Label(self.outdoor_frame, textvariable=self.outdoor_pressure_var, width=20).grid(row=4, column=1, sticky="w")

        # Weather condition symbol labels
        self.weather_labels = [Label(self.outdoor_frame) for _ in range(3)]
        for i, label in enumerate(self.weather_labels):
            label.grid(row=5, column=i, pady=10, sticky="w")

    def update_indoor_temperature(self,slider_value):
        '''
        Function to update indoor temperature display based on slider value
        Args: slider_value (int): the current value of the temperature adjustment slider.
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
        for i in range(8):  # Assuming a maximum of 8 rows in the indoor frame
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
        toggle_texts = ["Auto", "Heat On", "AC", "Auto Lights"]
        for i, text in enumerate(toggle_texts):
            toggle = self.create_toggle(self.indoor_frame, text)
            toggle.grid(row=i+2, column=0, columnspan=2, sticky="ew")
        
        # Toggle switch for power saving mode
        self.energy_saving_toggle = self.create_energy_saving_toggle(self.indoor_frame, "Energy Saving Mode")
        self.energy_saving_toggle.grid(row=10, column=0, columnspan=2, sticky="ew")
    
    def create_energy_saving_toggle(self, parent, text):
        '''
        Function to create a toggle switch button for energy-saving mode
        Args: self
              parent (frame): The parent widget in which the toggle button will be placed
              text (str): used as the label text for the toggle button
        '''
        var = IntVar(value=0)
        toggle = Label(parent, text=text, relief="raised", width=20, bg="red")
        toggle.var = var

        def on_click(event):
            ''' 
            Function to engage or disengage energy power saving by pressing a button
            Args: event, click event
            '''
            if toggle.var.get() == 0:
                toggle.config(relief="sunken", bg="green")
                toggle.var.set(1)
                self.activate_energy_saving_mode()
            else:
                toggle.config(relief="raised", bg="red")
                toggle.var.set(0)
                self.deactivate_energy_saving_mode()

        toggle.bind("<Button-1>", on_click)
        return toggle
    
    def activate_energy_saving_mode(self):
        '''Activates energy saving mode by changing GUI colors and increasing refresh interval.'''
        self.root.config(bg='dark grey')  # Simulate reduced brightness
        global refresh_time
        refresh_time = max(refresh_time, 1800000)  # Set a minimum 30-minute refresh interval
        self.refresh_time_var.set(f"{refresh_time/1000} s")

    def deactivate_energy_saving_mode(self):
        '''Deactivates energy saving mode by reverting GUI colors and refresh interval.'''
        self.root.config(bg='light grey')  # Revert to normal brightness
        global refresh_time
        refresh_time = 5000  # Reset to default refresh interval
        self.refresh_time_var.set(f"{refresh_time/1000} s")            

    def create_image_frame(self):
        '''Create and set up the frame for displaying camera images.'''
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

    def create_refresh_rate_frame(self):
        '''Create and set up the frame for controlling the refresh rate.'''
        self.refresh_rate_frame = LabelFrame(self.root, padx=2, pady=10)
        self.refresh_rate_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=10)
        self.configure_refresh_rate_frame()

    def configure_refresh_rate_frame(self):
        '''Configure the interior of the image frame for resizing.'''
        self.refresh_rate_frame.grid_rowconfigure(0, weight=1)
        for i in range(20):  # Assuming a maximum of 5 rows in any frame
            self.refresh_rate_frame.grid_columnconfigure(i, weight=1)

    def create_refresh_display(self):
        '''Create refresh button.'''
        Label(self.refresh_rate_frame, text="Refresh Rate:").grid(row=2, column=0, columnspan=5, sticky="ew",pady=4)
        desired_refresh_rate_display = Label(self.refresh_rate_frame, textvariable=self.refresh_time_var, width=4)
        desired_refresh_rate_display.grid(row=2, column=4, columnspan=5, sticky="ew",pady=4)

    def create_refresh_button_up(self):
        '''Create refresh button.'''
        self.refresh_rate_up = Button(self.refresh_rate_frame, text="▲", command=self.increase_refresh_time)
        self.refresh_rate_up.grid(row=2, column=10, sticky="ew", pady=2)

    def increase_refresh_time(self):
        ''' method for increasing refresh time'''
        global refresh_time
        if refresh_time < 120000:
            refresh_time += 1000
            self.refresh_time_var.set(f"{refresh_time} s")
    
    def create_refresh_button_down(self):
        ''' Create refresh button.'''
        self.refresh_rate_down = Button(self.refresh_rate_frame, text="▼", command=self.decrease_refresh_time)
        self.refresh_rate_down.grid(row=2, column=11, sticky="ew", pady=2)

    def decrease_refresh_time(self):
        '''method for decreasing refresh time'''
        global refresh_time
        if refresh_time > 1000:
            refresh_time -= 1000
            self.refresh_time_var.set(f"{refresh_time/1000} s")

    def create_refresh_button(self):
        '''Create refresh button'''
        self.refresh_button = Button(self.refresh_rate_frame, text="Refresh Data", command=self.refresh_data)
        self.refresh_button.grid(row=2, column=12, columnspan=8, sticky="ew", pady=8)

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

        # Check for extreme weather conditions
        self.check_for_extreme_weather()

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
    
    def check_for_extreme_weather(self):
        ''' Check the current weather data against the thresholds and display notifications for extreme conditions. '''
        temp = float(self.outdoor_temp_var.get().rstrip('°C'))
        humidity = float(self.outdoor_humidity_var.get().rstrip('%'))
        pressure = float(self.outdoor_pressure_var.get().rstrip(' hPa'))

        message = ""
        if not (EXTREME_TEMPERATURE_THRESHOLD[0] <= temp <= EXTREME_TEMPERATURE_THRESHOLD[1]):
            message += f"Extreme Temperature Alert: {temp}°C\n"
        if not (EXTREME_HUMIDITY_THRESHOLD[0] <= humidity <= EXTREME_HUMIDITY_THRESHOLD[1]):
            message += f"Extreme Humidity Alert: {humidity}%\n"
        if not (EXTREME_PRESSURE_THRESHOLD[0] <= pressure <= EXTREME_PRESSURE_THRESHOLD[1]):
            message += f"Extreme Pressure Alert: {pressure} hPa\n"

        if message:
            self.show_notification(message)

    def show_notification_extreme_weather(self, message):
        '''
        Display a notification message in the GUI.
        Args: self
              message (str): A string to be displayed in the notification message 
        '''
        notification_window = Toplevel(self.root)
        notification_window.title("Weather Alert")
        notification_window.geometry("300x200")
        Label(notification_window, text=message, justify=LEFT).pack(pady=20)
        Button(notification_window, text="Dismiss", command=notification_window.destroy).pack()
        

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
