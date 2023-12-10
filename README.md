# Weather Station Project
An all-inclusive weather station project developed on a Raspberry Pi 4 is included in this repository. An extensive set of features designed to provide control and monitoring of the environment is the primary goal of the project. The major emphasis is on gathering, analyzing, and providing a user interface for environmental data, both current and historical.

## Features:
1. Data Collection and Logging: 
Using BME280 sensors, continuously log indoor and outdoor temperature, humidity, light intensity, and air quality.
2. Sky Condition Analysis: 
Using image processing and a CNN model, analyze sky photos to detect clear, overcast, or wet conditions, as well as day or night.
3. Lighting and Temperature Control: 
Using LEDs, simulate dynamic lighting and temperature control depending on sensor data.
4. Air Quality Monitoring: 
Determine the quality of the air in both indoor and outdoor locations.
5. Graphical User Interface (GUI): 
A user-friendly GUI allows you to access real-time weather data, user control choices, and historical data visualization.
6. Energy-Saving Mode: 
Reduce energy usage and enhance environmental sustainability.

## Usage:
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




