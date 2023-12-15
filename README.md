# Weather Station/Smart Home Project
## Still working on this
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
4. Air Quality Monitoring:
Determine the outdoor air quality.
5. Graphical User Interface (GUI):
A user-friendly GUI allows the user to access real-time weather data, and control indoor heating, cooling, and lighting
6. Energy-Saving Mode:
Reduce energy usage and enhance environmental sustainability.

## Hardware

1. Raspberry Pi 4B
2. BME280 Sensor
3. Adafruit MiCS5524 air quality sensor
4. Magnetic reed switch and magnet
5. Raspberry Pi camera
6. Lead lights
7. Resistors
8. Breadboard

## Usage

1. Clone the repository to your RaspberryPi.
    In bash
    git clone git@github.ubc.ca:MECH-524-101-2023W1/weather_station_project.git
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

## Documentation

For instructions regarding setup, hardware requirements, and usage, please refer to documentation.

## License

The project is licensed under UBC License.

## Acknowledgement:

Many thanks to the open-source community and ChatGPT for supplying libraries and resources that were used in this project.

## Authors

1. Parmeet Brar:        Student ID: 20877288
2. Priyanshu Bhateja:   Student ID: 81567786
3. Halvard Ng:          Srudent ID: 41277492