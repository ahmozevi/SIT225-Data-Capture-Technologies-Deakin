import serial
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate('D:key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bookstoreproject-9b273-default-rtdb.firebaseio.com/'
})

# Set up Serial communication
ser = serial.Serial('COM4', 115200)
ser.flush()

# Reference to Firebase database
ref = db.reference('/gyroscope_data')

# Collect data
start_time = time.time()
try:
    while True:
        if time.time() - start_time > 1800:  # 30 minutes in seconds
            break
        
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Assuming data format is "X: value Y: value Z: value"
                try:
                    parts = line.split()
                    X = float(parts[1])
                    Y = float(parts[3])
                    Z = float(parts[5])
                    
                    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                    data = {
                        'timestamp': timestamp,
                        'X': X,
                        'Y': Y,
                        'Z': Z
                    }
                    # Upload data to Firebase
                    ref.push(data)
                    print(f"Uploaded data: {data}")
                except ValueError:
                    print("Error parsing line:", line)
except KeyboardInterrupt:
    print("Data collection stopped.")

# Close the serial connection
ser.close()
