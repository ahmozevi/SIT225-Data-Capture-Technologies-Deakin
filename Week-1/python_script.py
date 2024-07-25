import serial
import time
import random
from datetime import datetime

# Establish serial communication 
ser = serial.Serial('COM4', 9600)

def log_with_time(message):
    """Prints a message with the current time."""
    current_time = datetime.now().strftime('%H:%M:%S')
    print(f"{current_time} - {message}")

while True:
    # Send a random number to the Arduino
    number_to_send = random.randint(1, 5)
    ser.write(f"{number_to_send}\n".encode())
    log_with_time(f"Sent to Arduino: {number_to_send}")
    
    # Wait for Arduino's response
    response = ser.readline().decode().strip()
    log_with_time(f"Received from Arduino: {response}")
    
    # Log start of sleep
    log_with_time(f"Starting to sleep for {response} seconds.")
    
    # Sleep for the number of seconds received from Arduino
    time.sleep(int(response))
    
    # Log end of sleep
    log_with_time(f"Done sleeping for {response} seconds.")
