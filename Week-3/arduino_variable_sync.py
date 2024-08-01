import sys
import traceback
import random
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime  # Import datetime module

DEVICE_ID = "e55ec3fc-498c-4bbf-9217-a3fba6b46014"
SECRET_KEY = "ygwtuNtR7bUBWMeDQ9Pz6yFXz"

# File handle for appending data
file_handle = None

# Callback function on temperature change event.
def on_temperature_changed(client, value):
    global file_handle
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
    csv_string = f"{timestamp}, {value}\n"  # Create CSV string

    # Write CSV string to file
    if file_handle:
        file_handle.write(csv_string)
        file_handle.flush()  # Ensure data is written to file immediately

def main():
    global file_handle
    print("main() function")

    # Open file in append mode
    file_handle = open('temperature_data.csv', 'a')

    # Instantiate Arduino cloud client
    client = ArduinoCloudClient(
        device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY
    )

    # Register with 'temperature' cloud variable
    # and listen on its value changes in 'on_temperature_changed'
    # callback function.
    client.register(
        "temperature", value=None, 
        on_write=on_temperature_changed)

    # Start cloud client
    client.start()

if __name__ == "__main__":
    try:
        main()  # Main function which runs in an internal infinite loop
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
        print(f"{timestamp} - Exception occurred:")
        traceback.print_tb(exc_traceback, file=sys.stdout)  # Print traceback with timestamp
    finally:
        if file_handle:
            file_handle.close()  # Ensure file is properly closed
