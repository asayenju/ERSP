# Fatigue detector for Helmet (Predict different types of Head gestures)

## Motivations:
- Initially, we wanted to collect data for cycling motion among a big group of people
- We want to use a machine learning model to differentiate between normal cycling motion and fatigued cycling motion
- A fatigued cycling motion could be mimicked if we move and cycle if we close our eyes (obviously this must be done in a stationary cycle that we use in the gym)
- To transfer the data, we must use a wireless connection method such as bluetooth or Wifi to transfer it to our computers
- Then use different machine learning models to classify the motion between normal cycling motion and fatigued cycling motion
- Do real time testing and test it with other cyclists

## Problems faced:
- None of us knew how to code in C and use Espressif
- Even when we switched to python, bluetooth was too complex to implement in circuit python as it was very unreliable
- Sensors were unreliable
- Time constraints eventually led us to switch the project to classifying different type of head movements instead.

## Methods and Methodology:
- We used a ESP32-S3-DevKitC-1-N32R8 device as our microcontroller and connected it to an imu that tracks acceleration and gyroscope
![Esp32-s3 sensor](https://circuitpython.org/assets/images/boards/large/espressif_esp32s3_devkitc_1.jpg)
### Steps to set up the ESP32 device with circuit python:
- 
