import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime
import os

DEVICE_ID = "9ff2ed82-7b6f-4b5e-87f6-e12c177cd823"
SECRET_KEY = "9RHCZ6BM?xZxLRmi7r7w2W4jm"

# Define file paths for CSV storage in D:\\Downloads\\
file_X = 'D:\\Downloads\\accelerometer_X.csv'
file_Y = 'D:\\Downloads\\accelerometer_Y.csv'
file_Z = 'D:\\Downloads\\accelerometer_Z.csv'

# Helper function to write to a CSV file
def append_to_file(file_path, value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Check if the file exists and add header if not
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'a') as file:
            file.write("time,value\n")  # Write header

    with open(file_path, 'a') as file:
        file.write(f"{timestamp},{value}\n")

# Callback function for accelerometer_X changes
def on_accelerometer_X_changed(client, value):
    print(f"accelerometer_X: {value}")
    append_to_file(file_X, value)

# Callback function for accelerometer_Y changes
def on_accelerometer_Y_changed(client, value):
    print(f"accelerometer_Y: {value}")
    append_to_file(file_Y, value)

# Callback function for accelerometer_Z changes
def on_accelerometer_Z_changed(client, value):
    print(f"accelerometer_Z: {value}")
    append_to_file(file_Z, value)

# Main function to configure the ArduinoCloudClient
def main():
    print("main() function")

    try:
        # Instantiate Arduino cloud client
        client = ArduinoCloudClient(
            device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
        )

        # Register each accelerometer variable and listen for changes
        client.register("accelerometer_X", value=None, on_write=on_accelerometer_X_changed)
        client.register("accelerometer_Y", value=None, on_write=on_accelerometer_Y_changed)
        client.register("accelerometer_Z", value=None, on_write=on_accelerometer_Z_changed)

        # Start the cloud client to listen for incoming data
        client.start()
    except Exception as e:
        print(f"An error occurred: {e}")
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, file=sys.stdout)

if __name__ == "__main__":
    main()
