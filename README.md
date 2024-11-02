# ESPClimateBot


## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Usage](#usage)
    - [Telegram Commands](#telegram-commands)
    - [Local Display](#local-display)
4. [Hardware Components](#hardware-components)
5. [Circuit Diagram / Schematic](#circuit-diagram--schematic)
6. [Code Functionality](#code-functionality)
7. [Dependencies](#dependencies)
8. [Additional Notes](#additional-notes)
9. [Possible Use Cases](#possible-use-cases)
10. [Possible Future Improvements](#possible-future-improvements)
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


## Hardware Components

- **ESP32 Board**
- **AHT21 Temperature and Humidity Sensor (I2C)**
- **Arduino Uno**
- **16x2 LCD Display** for local data output
- **Potentiometer** for LCD brightness adjusting
- **Three 1kOhm Resistors** used as a voltage divider for serial communication between the boards 

## Circuit Diagram / Schematic

The circuit diagram for this project, detailing the connections between the ESP32, Arduino Uno, sensor, and LCD, is available in the `Circuit_diagram` directory in this GitHub repository. Please refer to this directory for a clear visual representation of the hardware setup, including pin configurations and wiring.


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
      
- **ESP32TELEGRAMBoT.ino** - ESP32 Code:
    - Connects the ESP32 to the specified Wi-Fi network.
    - Initializes and reads temperature and humidity data from the AHT21 sensor.
    - Hosts a CoAP server that responds to "sensor" endpoint requests with formatted temperature and humidity data.
    - Sends the sensor readings back to the CoAP client when requested.
    - Sends the sensor reading to an Arduino Uno via serial communication.
      
- **ArduinoUnoTelegramBotProject.ino** - Arduino Uno Code:
    - Interfaces with a LiquidCrystal display (LCD) to show temperature and humidity data received via serial communication.
    - Reads incoming data in the format of "temperature humidity" and displays it on a 16x2 LCD screen.

## Dependencies

ESPClimateBot relies on the following libraries and APIs for its core functionality:

- **ESP32 Libraries (for Arduino IDE)**
    - **Adafruit_AHTX0.h**: Used to read temperature and humidity data from the AHT10 or AHT20 sensor on the ESP32.
    - **WiFi.h**: Manages Wi-Fi connections, enabling the ESP32 to connect to a network.
    - **WiFiUdp.h**: Provides UDP communication support, which is essential for CoAP.
    - **coap-simple.h**: Implements CoAP (Constrained Application Protocol) for communication between devices, allowing low-power, efficient data exchange.

- **Python Libraries**
    - **python-telegram-bot**:This library provides a pure Python, asynchronous interface for the Telegram Bot API.
    - **CoAPthon3**: A Python library for CoAP protocol, making it possible to create CoAP clients and servers to handle lightweight data transfer between devices.
    - **aiocoap**: An advanced, asynchronous CoAP library in Python, suitable for applications that benefit from non-blocking CoAP messaging and efficient multi-client handling. `aiocoap` provides tools for creating CoAP-based communication in Python, supporting both synchronous and asynchronous CoAP calls.
    - **matplotlib**: Generates graphs and visualizations of temperature and humidity data.
    - **pandas**: Manages and processes CSV files, enabling easy data storage and retrieval of sensor readings.
  
- **APIs**:
    - **Telegram Bot API** – Enables seamless integration with Telegram, allowing the bot to send and receive messages, images, and commands directly within the Telegram app. This API provides the bot with essential functionalities such as handling commands (e.g., `/start`, `/help`), interacting with users in real time, and delivering sensor data and graphs as chat messages or images.

## Additional Notes

- **Operating System**:  
  This project and bot are intended to run on a Linux-based environment. The command-line interface in Linux is essential for the CoAP communication.
- **Network Requirements**:  For the ESP32 module and the server to communicate successfully, **both devices must be connected to the same local network**. This ensures they can establish a reliable CoAP connection for exchanging data.
- **Getting the Telegram Bot Token**:  
  To run this bot, you'll need a bot token from Telegram. You can get your bot token by chatting with the [BotFather](https://t.me/BotFather) on Telegram. Once there, follow the prompts to create a new bot, and BotFather will provide you with a unique API token. Keep this token secure, as it grants control over your bot.
- **LCD Display on a Separate Microcontroller**:  
  Using a dedicated microcontroller, like an Arduino Uno, to display sensor data on an LCD screen makes it easier to expand the system with additional sensors and actuators in the future. By offloading the display functionality, you free up the ESP32 to handle other tasks and manage more complex interactions. In this project, the LCD was not powering up as expected, possibly due to insufficient power from the ESP32’s pins. To improve reliability, consider using an I2C LCD, which requires fewer connections and simplifies wiring.

  
## Possible Use Cases

- **Home Climate Monitoring**: Users can place the ESP32 with the AHT21 sensor in their homes to monitor temperature and humidity remotely. It helps maintain optimal indoor climate conditions, which is essential for health, comfort, and even protecting furniture or electronics sensitive to humidity.
- **Greenhouse Management**: TeleTempBot can be used in greenhouses to monitor climate conditions, ensuring that temperature and humidity stay within ideal ranges for plant growth. It enables remote monitoring and reduces the need for constant physical checks, helping farmers or hobbyists respond promptly to adverse conditions.

## Possible Future Improvements

This project could be expanded in several ways to enhance its functionality and adaptability:

- **Additional Bot Commands**: New commands could be added to provide more insightful data analysis. For example, commands to calculate and return the average temperature or humidity for a specified day, week, or month would give users more contextual data. Further commands could also allow users to set thresholds and receive alerts when sensor readings go beyond specified limits.

- **Integration of More Sensors**: The ESP32 board can be wired with additional sensors, such as CO2, light, or soil moisture sensors, to broaden the types of environmental data collected. This would create a more comprehensive environmental monitoring system and enable users to track multiple parameters.

- **Remote Control of Actuators**: By connecting relays or other actuators to the ESP32, users could remotely control devices such as fans, heaters, or humidifiers through bot commands. This would allow users to respond to specific sensor readings by activating or deactivating equipment.

- **Automated Control Systems**: Expanding the server-side logic to implement automated control systems would further enhance the project. For instance, the server could be programmed to automatically activate or deactivate relays when specific environmental conditions are met (e.g., turning on a humidifier if humidity falls below a certain threshold). Such automation would increase the project’s utility and enable it to function as an autonomous climate control system.

These improvements would add flexibility, enhance usability, and provide a more robust platform for monitoring and controlling environmental conditions remotely.


## Resources

- **[Python Telegram Bot Library](https://python-telegram-bot.org/)** – Official documentation and guides for using `python-telegram-bot` to easily interact with the Telegram Bot API in Python.
- **[Telegram Bot Tutorial Video](https://www.youtube.com/watch?v=aNmRNjME6mE)** – A video guide that walks through the setup and functionality of a Telegram bot, which might help in understanding the BotFather setup and basic bot commands.
- **[IoT Course Lab - CoAP Communication](https://ocw.cs.pub.ro/courses/iothings/laboratoare/2022/lab8)** – This lab guide from the IoT course at the University POLITEHNICA of Bucharest provides insights into CoAP communication, detailing both theoretical aspects and hands-on instructions for implementing CoAP in IoT projects.
- **[CoAP Simple Library for ESP32](https://github.com/hirotakaster/CoAP-simple-library)** – This GitHub repository hosts a simple CoAP library designed for ESP32 devices, allowing easy setup for CoAP communication. It includes instructions, examples, and source code useful for integrating CoAP functionality with the ESP32.
- **[CoAPthon3](https://github.com/Tanganelli/CoAPthon3)** – A Python library for CoAP (Constrained Application Protocol) designed for building CoAP clients and servers. This resource includes detailed documentation and examples that facilitate integration with IoT devices.





