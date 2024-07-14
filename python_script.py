import serial
import time
import random

# Establish serial communication 
ser = serial.Serial('COM4', 9600)

while True:
    # Send a random number to the Arduino
    number_to_send = random.randint(1, 5)
    ser.write(f"{number_to_send}\n".encode())
    print(f"Sent to Arduino: {number_to_send}")
    
    # Wait for Arduino's response
    response = ser.readline().decode().strip()
    print(f"Received from Arduino: {response}")
    
    # Sleep for the number of seconds received from Arduino
    time.sleep(int(response))
