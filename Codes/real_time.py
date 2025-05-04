import serial
import pickle
import numpy as np
import time
import re
from collections import deque

# Constants
SERIAL_PORT = 'COM17'
BAUD_RATE = 115200
WINDOW_SIZE = 100  # Number of samples per prediction
PREDICTION_INTERVAL = 0.5  # Seconds between predictions

class RealTimeGestureClassifier:
    def __init__(self):
        # Initialize serial connection
        self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
        
        # Load the trained SVM model
        with open('svm_model.pk1', 'rb') as file:
            self.model = pickle.load(file)
        
        # Data buffer
        self.data_buffer = deque(maxlen=WINDOW_SIZE)
        self.last_prediction_time = time.time()
        
        # Gesture labels (must match your training labels)
        self.labels = ['sitting_still', 'sitting_nodding_up_down', 
                      'sitting_nodding_side_to_side', 'sitting_nodding_diagonal']
    
    def read_sensor_data(self):
        """Read and parse data from serial port."""
        try:
            data = self.ser.readline().decode('utf-8').strip()
            if data:
                row = data.split(",")
                if len(row) >= 6:
                    cleaned_row = [re.sub(r'[^\d.-]', '', value) for value in row[:6]]
                    return list(map(float, cleaned_row))
        except Exception as e:
            print(f"Serial read error: {e}")
        return None
    
    def extract_features(self):
        """Extract features in same format as training."""
        window_array = np.array(self.data_buffer)
        features = [
            np.mean(window_array[:, 0]), np.std(window_array[:, 0]),  # accel_x
            np.mean(window_array[:, 1]), np.std(window_array[:, 1]),  # accel_y
            np.mean(window_array[:, 2]), np.std(window_array[:, 2]),  # accel_z
            np.mean(window_array[:, 3]), np.std(window_array[:, 3]),  # gyro_x
            np.mean(window_array[:, 4]), np.std(window_array[:, 4]),  # gyro_y
            np.mean(window_array[:, 5]), np.std(window_array[:, 5])   # gyro_z
        ]
        return np.array(features).reshape(1, -1)
    
    def predict_gesture(self):
        """Predict gesture from current window data."""
        if len(self.data_buffer) < WINDOW_SIZE:
            return None
        
        features = self.extract_features()
        prediction_idx = self.model.predict(features)[0]
        return self.labels[prediction_idx]
    
    def run(self):
        """Run the real-time classification."""
        try:
            print("Starting real-time gesture classification...")
            print("Press Ctrl+C to stop\n")
            
            while True:
                # Read sensor data
                sensor_data = self.read_sensor_data()
                if sensor_data:
                    self.data_buffer.append(sensor_data)
                    
                    # Make predictions at regular intervals
                    current_time = time.time()
                    if current_time - self.last_prediction_time > PREDICTION_INTERVAL:
                        self.last_prediction_time = current_time
                        gesture = self.predict_gesture()
                        if gesture:
                            print(f"\rCurrent Gesture: {gesture.ljust(30)}", end='', flush=True)
                
                # Small delay to prevent CPU overload
                time.sleep(0.001)
                
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self.ser.close()

if __name__ == "__main__":
    classifier = RealTimeGestureClassifier()
    classifier.run()