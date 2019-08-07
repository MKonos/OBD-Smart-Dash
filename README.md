# OBD Smart Dash

![Intro picture](/pictures/1.PNG)

## Description

The goal of this project was to combine 5 seperate compute units, or "buses" together for form a network of devices that perform a task. In this case we took inspiration from the automotive implementation of CANBUS, a communication architecture in which various microcontrollers and sensors in a car report to a central "brain" that adjusts things like suspension or automatic wipers based on what the sensors encounter. The car communicates with the device using serial UART and does so through a modified OBD2 adapter designed to fit most cars since the 1990s. The car used was a 2010 Hyundai Genesis, but is compatible with almost any car on the market. 

## Hardware Used

Arduino Uno x3
  - Gyroscope for measuring G-forces while driving
  - LCD screen
  - GPS module
Arduino Mega
  - POGO pin shield 
  - SD card
Raspberry Pi B running Raspian
  - POGO pin touch display
  
![Intro picture](/pictures/4.jpg)

---
  
# Modules

---

## Data Logger 

The Arduino Mega served as the brain of the system and stored all onboard data until storage capacity was 95% filled up. Data would then be deleted starting with the oldest records. Polling rate of the sensors was set to every half second. 




## Satellite Sensors/Loggers

Each Arduino Uno performed one task per board:
  - Gather data via obd and pass it on to the data logger while also debugging information directly to the LCD screen 
![Intro picture](/pictures/5.PNG)

  - gather GPS data and transfer it to the data logger
![Intro picture](/pictures/6.png)

  - gather acceleromete data and pass it on to the data logger


## Display Module

The Raspberry Pi served as the display and interface. Using a touch display the user could launch the stats monitor screen to see the data sensors in the car were reporting as well as the additional sensors we added. The information from the data logger was sent to the Pi via USB connection and then processed by a webserver. A shortcut on the desktop of the Pi contained a URL to the webpage where the car's stats are displayed. 


 
## Video

https://www.youtube.com/watch?v=lq7yIZGjKSU&t=77s
