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

### Steps for data collection and machine learning model
1. clone repository:
```
git clone https://github.com/asayenju/ERSP.git
```
2. Install all requirements
```
pip install -r requirements.txt
```

# Explaining what the main important files do
## data_collection.py:
- Collect data from the specific serial number as you can modify the code by going to device managers to check which port the microcontroller is connected to.
- Baud rate is the speed at which data is transmitted over serial communication, and we set it to 9600, which is common for basic projects but can become higher depending on the microcontroller.
- This code write the transmitted data into text files starting from file 1 to as many file as you want and you can modify this in the while loop.
- It will collect data for 10 seconds and during those 10 seconds, it will read from the serial port collect the data and write it in the file.
- You can modify the print statement in the end to write how many files of data you collected.

## truncate.py:
- Since machine learning requires the text files to be of the same number of lines, we truncated every file to 600 lines.

## rename_file.py:
- Some of our text files had different names, so this code is mainly to rename it to a consistent file name.

## svm.py:
1. Data Loading & Feature Extraction:
- load_and_extract_features(file_path):
  - Reads a .txt file containing sensor data (accelerometer + gyroscope).
  - Extracts mean & standard deviation for each axis (accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z).
  - Returns a 12-dimensional feature vector per file.

- prepare_dataset(data_dir):
    - Organizes data into 4 gesture classes:
        - sitting_still (Label 0)
        - sitting_nodding_up_down (Label 1)
        - sitting_nodding_side_to_side (Label 2)
        - sitting_nodding_diagonal (Label 3)
    - Splits data into 70% training & 30% testing per class.
    - Returns X_train, X_test, y_train, y_test.

2. Dataset Analysis:
- Prints dataset shapes (e.g., Train set -> Features: (280, 12), Labels: (280,)).
- Checks class distribution (ensures balanced data).
- Computes feature statistics (mean & std dev).

3. Model Training (SVM):
- Uses Radial Basis Function (RBF) kernel (SVC(kernel='rbf')).
- Fits the model on X_train, y_train.

4. Evaluation:
- Accuracy: Computes test accuracy (e.g., Model Accuracy: 95.00%).
- Classification Report:
  - Shows precision, recall, F1-score per class.
- Confusion Matrix:
  - Visualizes true vs. predicted labels.
- Uses seaborn for an annotated heatmap with large fonts.

5. Output:
- Displays confusion matrix (plt.show()).
- Helps assess model performance on different gestures.

## knn.py:
1. Data Loading & Feature Extraction:
- load_and_extract_features(file_path):
  - Reads .txt files containing accelerometer (x,y,z) and gyroscope (x,y,z) data.
  - Extracts mean and standard deviation for each axis → 12 features per file.
- prepare_dataset(data_dir):
  - Organizes data into 4 classes:
    - sitting_still (Label 0)
    - sitting_nodding_up_down (Label 1)
    - sitting_nodding_side_to_side (Label 2)
    - sitting_nodding_diagonal (Label 3)
  - Splits data into 70% training, 30% testing per class.

2. Preprocessing (Critical for KNN)
- StandardScaler normalizes features:
  - Ensures all features contribute equally to distance calculations.
  - Fit on X_train, then transform X_train and X_test.

4. KNN Model Training
- Hyperparameters:
  - n_neighbors=5: Classifies based on 5 closest data points.
  - weights='distance': Closer neighbors have more influence.
  - metric='euclidean': Uses Euclidean distance for proximity.
- Training:
  - knn_model.fit(X_train_scaled, y_train) → Trains on scaled data.

5. Model Evaluation
- Accuracy:
  - accuracy_score(y_test, y_pred) → Reports test accuracy (e.g., 95.00%).
- Classification Report:
  - Shows precision, recall, F1-score for each gesture class.
- Confusion Matrix:
  - Visualizes true vs. predicted labels (heatmap).

6. Optional: Finding Optimal k
- Tests k values from 1 to 14 and plots accuracy trends.
- Helps identify the best n_neighbors for the dataset.

7. Model & Scaler Saving
- joblib.dump() saves:
  - Trained KNN model (knn_model.pk1).
  - Fitted scaler (knn_scaler.pk1) → Must be reused during inference.
