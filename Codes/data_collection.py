import serial
import time

ser = serial.Serial('COM17', 9600)  # Replace with your port and baud rate

file_number = 1# Starting file number

while file_number <= 2:
    filename = f'sitting_nod_side_toide{file_number}.txt'
    
    with open(filename, 'w', encoding='utf-8') as file:
        start_time = time.time()
        
        print(f"Recording data to {filename}...")
        
        while time.time() - start_time < 10:  # Record for 10 seconds
            if ser.in_waiting:
                data = ser.readline()
                decoded_data = data.decode('utf-8').strip()
                file.write(decoded_data + '\n')
    
    print(f"Data saved to {filename}")
    file_number += 1  # Move to the next file

ser.close()
print("All data collection complete (files 21-100).")