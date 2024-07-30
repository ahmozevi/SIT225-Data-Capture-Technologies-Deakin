import serial
import time
import csv
from datetime import datetime

# Establish serial communication with Arduino
ser = serial.Serial('COM3', 9600)
time.sleep(2)  # Wait for the serial connection to initialize

# Create a CSV file with the current timestamp in the filename
filename = f"HC_SR04_data_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"

# Open CSV file in append mode
with open(filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Distance (cm)"])  

    # Collect data for 30 minutes (1800 seconds)
    start_time = time.time()
    while time.time() - start_time < 1800:
        if ser.in_waiting > 0:
            raw_data = ser.readline().decode().strip()
            
            # Extract the numeric distance value from the raw data
            if raw_data.startswith("Distance: "):
                distance = raw_data.split("Distance: ")[1] + " cm"
            else:
                distance = "Invalid data"
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, distance])
            print(f"{timestamp} {distance}")  # Updated print statement
        time.sleep(1)  # Collect data every second

print("Data collection complete.")
