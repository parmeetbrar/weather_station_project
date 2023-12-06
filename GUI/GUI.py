#######################################################################################################################

# Project: Weather Station Project
# File: Graphical User Interface (GUI)

# Author: Parmeet Brar
# Purpose:       
# Description: 
# Date last edited: 11/24/2023

#######################################################################################################################

# Imports

from tkinter import Tk, Label, Scale, HORIZONTAL, LabelFrame, Button, StringVar, IntVar, Canvas
from PIL import Image, ImageTk
import random
import os

# Function to create a Toggle Switch
def create_toggle(parent, text):
    var = IntVar(value=0)
    toggle = Label(parent, text=text, relief="raised", width=8, bg="red")
    toggle.var = var

    def on_click(event):
        if toggle.var.get() == 0:
            toggle.config(relief="sunken", bg="green")
            toggle.var.set(1)
        else:
            toggle.config(relief="raised", bg="red")
            toggle.var.set(0)
    
    toggle.bind("<Button-1>", on_click)
    return toggle

# Function to load and resize images using PIL
def load_weather_image(filename, size=(50, 50)):  # Adjust the size as needed
    img = Image.open(os.path.join(base_folder, filename))
    img = img.resize(size, Image.Resampling.LANCZOS)  # Resize image using LANCZOS filter
    return ImageTk.PhotoImage(img)

# Function to determine weather condition based on sensor values
def determine_weather_condition(temp, humidity, wind_speed):
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

# Function to refresh data with random values and update weather symbol
def refresh_data():
    # Generate random sensor values
    temp = random.randint(-10, 40)
    humidity = random.randint(0, 100)
    wind_speed = random.randint(0, 150)

    # Update outdoor data with random sensor values
    outdoor_temp_var.set(f"{temp}°C")
    outdoor_humidity_var.set(f"{humidity}%")
    outdoor_wind_var.set(f"{wind_speed} km/h")
    outdoor_pressure_var.set(f"{random.randint(950, 1050)} hPa")

    # Update indoor temperature display
    current_temp_var.set(f"{random.randint(16, 30)}°C")

    # Determine weather conditions based on sensor values
    current_conditions = determine_weather_condition(temp, humidity, wind_speed)

    # Update the weather condition images
    for label, condition in zip(weather_labels, current_conditions):
        label.config(image=weather_images[condition])
        label.image = weather_images[condition]

    # Clear any unused weather labels
    for label in weather_labels[len(current_conditions):]:
        label.config(image='')
        label.image = None

# Create the main window
root = Tk()
root.title("Climate Control GUI")
root.geometry("800x600")  # Set the window size

# Row and Column configuration for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Define the file path for the weather symbols
base_folder = r"C:\Users\ASUS\Desktop\GUI"

# Load weather condition symbols using PIL
weather_images = {
    'cloud': load_weather_image('cloud.png'),
    'cold': load_weather_image('cold.png'),
    'rain': load_weather_image('rain.png'),
    'sunny': load_weather_image('sunny.png'),
    'wind': load_weather_image('wind.png')
}

# Outdoor data variables
outdoor_temp_var = StringVar()
outdoor_humidity_var = StringVar()
outdoor_wind_var = StringVar()
outdoor_pressure_var = StringVar()

# Indoor temperature variable
current_temp_var = StringVar()

# Outdoor frame
outdoor_frame = LabelFrame(root, text="OUTDOOR", font=("Helvetica", 16), padx=10, pady=10)
outdoor_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

# Configure the interior of the frames for resizing
for i in range(5):  # Assuming a maximum of 5 rows in any frame
    outdoor_frame.grid_rowconfigure(i, weight=1)
outdoor_frame.grid_columnconfigure(0, weight=1)
outdoor_frame.grid_columnconfigure(1, weight=1)

# Outdoor data labels
Label(outdoor_frame, text="Temperature (°C):").grid(row=0, column=0, sticky="e")
Label(outdoor_frame, textvariable=outdoor_temp_var, width=20).grid(row=0, column=1, sticky="w")

Label(outdoor_frame, text="Humidity (%):").grid(row=1, column=0, sticky="e")
Label(outdoor_frame, textvariable=outdoor_humidity_var, width=20).grid(row=1, column=1, sticky="w")

Label(outdoor_frame, text="Windspeed (km/h):").grid(row=2, column=0, sticky="e")
Label(outdoor_frame, textvariable=outdoor_wind_var, width=20).grid(row=2, column=1, sticky="w")

Label(outdoor_frame, text="Pressure:").grid(row=3, column=0, sticky="e")
Label(outdoor_frame, textvariable=outdoor_pressure_var, width=20).grid(row=3, column=1, sticky="w")

# Weather condition symbol labels
weather_labels = [Label(outdoor_frame) for _ in range(3)]
for i, label in enumerate(weather_labels):
    label.grid(row=4, column=i, pady=10, sticky="w")
    
# Indoor frame
indoor_frame = LabelFrame(root, text="INDOOR", font=("Helvetica", 16), padx=10, pady=10)
indoor_frame.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

# Configure the interior of the indoor frame for resizing
for i in range(7):  # Assuming a maximum of 7 rows in the indoor frame
    indoor_frame.grid_rowconfigure(i, weight=1)
indoor_frame.grid_columnconfigure(0, weight=1)
indoor_frame.grid_columnconfigure(1, weight=1)

# Indoor temperature display and slider
Label(indoor_frame, text="Current Temperature:").grid(row=0, column=0, sticky="e")
current_temp_display = Label(indoor_frame, textvariable=current_temp_var, width=20)
current_temp_display.grid(row=0, column=1, sticky="w")

Label(indoor_frame, text="Adjust Temperature:").grid(row=1, column=0, sticky="e")
Scale(indoor_frame, from_=0, to=40, orient=HORIZONTAL).grid(row=1, column=1, sticky="ew")

# Indoor toggle switches
toggle_texts = ["Auto", "Heat On", "AC", "Auto Lights", "Energy Saving Mode"]
for i, text in enumerate(toggle_texts):
    toggle = create_toggle(indoor_frame, text)
    toggle.grid(row=i+2, column=0, columnspan=2, sticky="ew")

# Image display frame for camera image
image_frame = LabelFrame(root, text="Camera Image", font=("Helvetica", 16), padx=10, pady=10)
image_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Configure the interior of the image frame for resizing
image_frame.grid_rowconfigure(0, weight=1)
image_frame.grid_columnconfigure(0, weight=1)

# Placeholder for the camera image
camera_canvas = Canvas(image_frame, width=760, height=240, bg='light blue')
camera_canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Display placeholder text for camera image, you would update this with an actual image
camera_canvas.create_text(380, 120, text="Camera Image Placeholder", font=("Helvetica", 16))

# Refresh button to update data with random values
refresh_button = Button(root, text="Refresh Data", command=refresh_data)
refresh_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

# Initialize outdoor data with random values
refresh_data()  # Call once to populate with initial random data

# Run the application
root.mainloop()
