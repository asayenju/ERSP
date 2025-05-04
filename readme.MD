# Fatigue detector for Helmet (Predict different types of Head gestures)

## Motivations:
- Initially, we wanted to collect data for cycling motion among a big group of people
- We want to use a machine learning model to differentiate between normal cycling motion and fatigued cycling motion
- A fatigued cycling motion could be mimicked if we move and cycle if we close our eyes (obviously this must be done in a stationary cycle that we use in the gym)
- To transfer the data, we must use a wireless connection method such as Bluetooth or Wifi to transfer it to our computers
- Then use different machine learning models to classify the motion between normal cycling motion and fatigued cycling motion
- Do real-time testing and test it with other cyclists

## Problems faced:
- None of us knew how to code in C and use Espressif
- Even when we switched to Python, Bluetooth was too complex to implement in circuit Python as it was very unreliable
- Sensors were unreliable
- Time constraints eventually led us to switch the project to classifying different head movements instead.

## Methods and Methodology:
- We used a ESP32-S3-DevKitC-1-N32R8 device as our microcontroller and connected it to an imu (MPU6050) that tracks acceleration and gyroscope
### Steps to set up the ESP32 device with circuit python:
<div align="center" style="display: flex; justify-content: space-between;">
  <div style="margin: 10px; ">
    <strong>ESP32-S3-DevKitC</strong><br>
    <img src="https://circuitpython.org/assets/images/boards/large/espressif_esp32s3_devkitc_1.jpg" alt="ESP32 Board" width="250"/>
  </div>
  <div style="margin: 10px;">
    <strong>MPU6050 IMU</strong><br>
    <img src="https://store.flytron.com/cdn/shop/products/986_580x.jpg?v=1581362322" alt="MPU6050 Sensor" width="250"/>
  </div>
</div>

## Step 1:
1. First, connect the four wires in the IMU and plug them into these pins: UCC, GND, SCL, and SDA. Make sure you don't tangle them.
2. Now the other end of the wires needs to be connected to the microcontroller in this corresponding manner: UCC-3V (last pin), GND-G, SCL-0, SDA-1

## Step 2:
1. Plug the separate wire containing the USB micro-c to the USB of the microcontroller and the USB type A into your laptop (before doing that make sure that the pins are plugged in the correct order)
2. Go to https://circuitpython.org/board/espressif_esp32s3_devkitc_1_n32r8/ and open the installer to install full circuit python
3. Follow the instructions also you might need to press the boot two times during this process to find Drive D and you might want to do this multiple times or just unplug the device and plug it back in
4. Installation is probably the hardest part so make sure to do it multiple times

## Step 3:
1. Open the folder of your device
2. Download the correct version bundle from here https://circuitpython.org/libraries
3. Paste the lib folder from this bundle to your device
4. Paste the code from the ESP32 code directory in this repo into a new file called code.py which you can create

## Step 4 (Optional):
1. To test this you can use Putty to test if it is passing the data so you can download the software here: https://www.putty.org/
2. After installing putty change the connection type to serial
3. Go to the device manager to see what port the device is connected to (i.e COM17)
4. Write your serial line in putty as the port and press open
5. You can see huge lines of acceleration and gyroscope data (different dimensions) in the form of ax, ay, az, gx, gy, gz
6. Play around with the imu to see if the data changes if you move the device in different motions


