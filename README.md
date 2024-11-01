# ESPClimateBot


## Table of Contents

1. [Overview](#overview)
2. [Dependencies](#dependencies)
3. [Features](#features)
4. [Bot Commands / Usage](#bot-commands--usage)
    - [Telegram Commands](#telegram-commands)
    - [Local Display](#local-display)
5. [Installation](#installation)
6. [Hardware Components](#hardware-components)
7. [Circuit Diagram / Schematic](#circuit-diagram--schematic)
8. [Code Functionality](#code-functionality)
9. [Possible Future Improvements](#possible-future-improvements)
10. [Possible Use Cases](#possible-use-cases)
11. [Resources](#resources)


## Overview

ESPClimateBot is a convenient solution for remote monitoring of environmental data. It connects to Telegram, allowing users to retrieve temperature and humidity data through simple commands. The project uses the ESP32 microcontroller with an AHT21 sensor over I2C to gather data, which is displayed locally and available remotely via Telegram commands.


## Features

- **Remote Access**: Retrieve temperature and humidity data through bot commands in Telegram.
- **Data Collecting**: Sensor data acquisition and storage.
- **Accurate Readings**: Utilizes the AHT21 sensor for precise temperature and humidity measurements.
- **Local Display**: Real-time data is displayed on the attached LCD screen.


## Usage

### Telegram Bot Commands

- **/sensor_data**: Retrieves real-time temperature and humidity data from the sensor.
- **/climate_graph**: Returns a graph showing the evolution of temperature and humidity over a specified period of time.
- **/start**: Sends a welcome message.
- **/help**: Provides information about available commands.
- **/send_photo**: Sends a possible profile photo for the bot.
- **/caps**: Returns the given text in all uppercase letters.
- **/echo**: Repeats the given text exactly as provided.


### Local Display

The local display shows the values for temperature(°C) and the relative humidity(%) given by the AHT21 sensor. The display is updated every 2 seconds.


## Installation

1. Clone the Repository
2. Install Required Libraries
3. Flash the ESP32(and Arduino Uno)
4. Configure Telegram Bot - Create a new bot on Telegram via BotFather and obtain your bot token and update your bot token and Wi-Fi credentials in the code files.

## Hardware Components

- **ESP32 Board**
- **AHT21 Temperature and Humidity Sensor (I2C)**
- **16x2 LCD Display** for local data output



## Circuit Diagram / Schematic

Include the circuit diagram or schematic here, or a link to it if hosted externally.


## Code Functionality
- **bot.py** - Main File:
    - Sets up logging and initializes the Telegram bot.
    - Implements bot commands for data retrieval, visualization, and basic interaction.
    - Logs sensor data to a CSV file and schedules periodic data retrieval.
    
- **connectivity.py** - CoAP Connectivity:
    - Connects to an ESP32 device via CoAP protocol to request sensor data.
    - Sends CoAP requests every 3 seconds to retrieve sensor readings from the ESP32.
    - Uses the `coap-client` command to communicate with the ESP32 and captures the device's response for logging.

- **csvHandling.py** - CSV Class:
    - Initializes and logs temperature and humidity data to a CSV file.
    - Retrieves temperature and humidity readings within a specified date range.
    - It has a function that plots daily average temperature and humidity trends, saving the plot as an image.

## Dependencies

TeleTempBot relies on the following libraries and APIs:

- **ESP32 Libraries** (for Arduino IDE):
  - `Adafruit_AHTX0.h` – for reading data from the AHT21 temperature and humidity sensor.
  - `WiFi.h` `WiFiUdp.h` `coap-simple.h` 
- **Python Libraries**:
  - `CoAPthon3` and `aiocoap` – for 
  - `matplotlib` – for creating a local web server if needed.
  - `pandas` - for handling CSV files

- **APIs**:
  - **Telegram Bot API** – used to communicate with Telegram and enable bot functionalities.


## Possible Future Improvements

Ideas for potential improvements:
- Improvement 1
- Improvement 2


## Possible Use Cases

- **Home Climate Monitoring**: Users can place the ESP32 with the AHT21 sensor in their homes to monitor temperature and humidity remotely. It helps maintain optimal indoor climate conditions, which is essential for health, comfort, and even protecting furniture or electronics sensitive to humidity.
- **Greenhouse Management**: TeleTempBot can be used in greenhouses to monitor climate conditions, ensuring that temperature and humidity stay within ideal ranges for plant growth. It enables remote monitoring and reduces the need for constant physical checks, helping farmers or hobbyists respond promptly to adverse conditions.




## Resources

Provide links to any resources, tutorials, or documentation that may be helpful for understanding or extending the project.


