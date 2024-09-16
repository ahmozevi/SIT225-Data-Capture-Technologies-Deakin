import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime
import os
import time

DEVICE_ID = "9ff2ed82-7b6f-4b5e-87f6-e12c177cd823"
SECRET_KEY = "9RHCZ6BM?xZxLRmi7r7w2W4jm"

# Define file path for CSV storage
file_path = 'D:\\Downloads\\accelerometer_data.csv'

# Helper function to write to a CSV file with retry mechanism
def append_to_file(x_value, y_value, z_value, max_retries=5, delay=1):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    retries = 0
    while retries < max_retries:
        try:
            # Check if the file exists and add header if not
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                with open(file_path, 'a') as file:
                    file.write("time,X,Y,Z\n")  # Write header

            with open(file_path, 'a') as file:
                file.write(f"{timestamp},{x_value},{y_value},{z_value}\n")
            break
        except IOError as e:
            print(f"IOError: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
            retries += 1
    if retries == max_retries:
        print("Max retries reached. Failed to write to file.")

# Variables to store latest values
x_value = None
y_value = None
z_value = None

# Callback function for accelerometer_X changes
def on_accelerometer_X_changed(client, value):
    global x_value
    x_value = value
    print(f"accelerometer_X: {value}")
    if y_value is not None and z_value is not None:
        append_to_file(x_value, y_value, z_value)

# Callback function for accelerometer_Y changes
def on_accelerometer_Y_changed(client, value):
    global y_value
    y_value = value
    print(f"accelerometer_Y: {value}")
    if x_value is not None and z_value is not None:
        append_to_file(x_value, y_value, z_value)

# Callback function for accelerometer_Z changes
def on_accelerometer_Z_changed(client, value):
    global z_value
    z_value = value
    print(f"accelerometer_Z: {value}")
    if x_value is not None and y_value is not None:
        append_to_file(x_value, y_value, z_value)

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
