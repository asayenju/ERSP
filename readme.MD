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
  - Shows precision, recall, and F1-score for each gesture class.
- Confusion Matrix:
  - Visualizes true vs. predicted labels (heatmap).

6. Optional: Finding Optimal k
- Tests k values from 1 to 14 and plots accuracy trends.
- Helps identify the best n_neighbors for the dataset.

7. Model & Scaler Saving
- joblib.dump() saves:
  - Trained KNN model (knn_model.pk1).
  - Fitted scaler (knn_scaler.pk1) → Must be reused during inference.

## real_time.py (SVM Model only):
1. Purpose:
- Real-time gesture recognition using a trained SVM model on streaming accelerometer/gyroscope data from a serial port (e.g., Arduino/IMU sensor).

2. Key Components:
- Serial Communication:
  - Reads data from COM17 at 115200 baud rate.
  - Parses comma-separated values (6 columns: 3 accelerometer + 3 gyroscope axes).
- Data Processing:
  - Sliding Window: Buffers 100 samples (WINDOW_SIZE) for feature extraction.
  - Feature Extraction: Computes mean/std for each axis (12 features total) to match training format. 
- Model Inference:
  - Loads a pre-trained SVM model (svm_model.pk1).
  - Predicts gestures every 0.5 seconds (PREDICTION_INTERVAL).

3. Workflow
- Initialize:
  - Open serial connection.
  - Load SVM model.
  - Set up a circular buffer (deque) for sensor data.
- Read Data:
  - Continuously reads and cleans serial data (handles errors/noise).
- Feature Extraction:
  - When buffer reaches WINDOW_SIZE, computes features (mean/std per axis).
- Prediction:
  - SVM predicts gesture (e.g., sitting_still, nodding_up_down).
  - Prints results in real-time.

4. Gesture Labels
- Maps predicted class indices to human-readable labels:
```
['sitting_still', 'sitting_nodding_up_down', 
 'sitting_nodding_side_to_side', 'sitting_nodding_diagonal']
```

5. Error Handling:
- Serial Errors: Skips malformed data.
- KeyboardInterrupt: Gracefully stops on Ctrl+C.

6. Critical settings:
- WINDOW_SIZE=100: Balances latency and accuracy.
- PREDICTION_INTERVAL=0.5: Controls prediction frequency.
- Baud Rate: Must match the sender device (e.g. ESP32).

7. Output:
- Prints predicted gestures in real-time:
```
Current Gesture: sitting_nodding_up_down
```

## other python files:
- Raw scores help show the data in line graphs
- Spectrogram helps show the data in terms of different frequencies
- random_forest_classifier is just another experimental machine learning file and we don't think it's accurate
- Bluetooth collection is to collect data using Bluetooth and this was not very reliable
- Bluetooth devices is a code to find Bluetooth devices around your device but it couldn't find the microcontroller

### Results and Conclusion:
- Confusion Matrix for SVM model:
  <div align="center" style="margin: 20px 0;">
  <div>
    <img src="svm_confusion matrix.png" alt="Gesture Data Visualization" width="400"/>
  </div>
</div>

- Here, it mistakes 30% of sitting_still as sitting_nodding_side_to_side.
- Observation: The model was trained with the first 70 text files and tested with the last 30 text files. When I trained it with 70 random files and tested it with 30 random files which were all unused, I got 100% model accuracy.

- Confusion Matrix for Knn Model:
  <div align="center" style="margin: 20px 0;">
  <div>
    <img src="Figure_1.png" alt="Gesture Data Visualization" width="400"/>
  </div>
</div>

- Here, KNN is more accurate as it mistakes 7 text files of sitting_still as sitting_nodding_side_to_side.
- Observation: Same observation with SVM, training with 70 random files and testing it with 30 random files will get me 100% model accuracy.

### Future Works:
## 1. Machine Learning for Actual Fatigue Classification:
- Collect Data for different types of motion while cycling normally
- Collect Data for different types of motion while cycling in a stationary bike with eyes closed
- Use SVM, Random CLassifier, and KNN for the best and fastest predictions as we compare between these different models
- Do real-time prediction

## 2. Bluetooth Integration:
- Using BLE, learn how to implement Bluetooth properly by watching YouTube videos or reading through documentation thoroughly
- Alternatively, switch to programming in C or Espressif and learn how to use Bluetooth to get the data

## 3. Renewable Energy Integration:
- Using solar panels to power up the sensor or other types of renewable energy

## 4. Real-time testing:
- testing it if it detects fatigue or not

## 5. Mobile app:
- Developing an app or software that sends push notifications if the data sent to the device detects fatigue.

## 6. 3D printing:
- Designing and 3D printing a structure that holds the sensor universally for all helmets.

## 7. Deployment and testing
- Deploying the app and testing the helmet for many bikers




