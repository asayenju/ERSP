from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import time
import sys

ble = BLERadio()
uart_connection = None

# Open a text file to write the data
with open("walking_eyes_open_nodding.txt", "w") as file:
    start_time = time.time()  # Record the start time

    while True:
        if not uart_connection:
            print("Trying to connect...")
            advertisements = list(ble.start_scan(ProvideServicesAdvertisement, timeout=10))
            ble.stop_scan()  # Stop scanning before iterating
            
            for adv in advertisements:
                print(f"Found: {adv.complete_name}, Services: {adv.services}")
                if UARTService in adv.services:
                    try:
                        uart_connection = ble.connect(adv)
                        print("Connected")
                        break
                    except RuntimeError as e:
                        print(f"BLE connection failed: {e}")
                        uart_connection = None

        if uart_connection and uart_connection.connected:
            uart_service = uart_connection[UARTService]
            while uart_connection.connected:
                try:
                    # Read data from UART
                    data = uart_service.readline().decode("utf-8").strip()
                    if data:
                        print(data)  # Print data to console
                        file.write(data + "\n")  # Write data to file

                    # Check if 10 seconds have passed
                    if time.time() - start_time >= 10:
                        print("10 seconds have passed. Stopping data collection.")
                        file.close()
                        sys.exit()  # Exit safely
                except Exception as e:
                    print(f"Error reading from UART: {e}")
                    break  # Exit loop if there's an issue

        print("Disconnected! Restarting scan...")
