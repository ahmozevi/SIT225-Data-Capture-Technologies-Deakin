import sys
import traceback
from arduino_iot_cloud import ArduinoCloudClient
import asyncio
from datetime import datetime
import os
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import threading
import plotly.io as pio
import pandas as pd
import matplotlib.pyplot as plt
import signal

DEVICE_ID = "9ff2ed82-7b6f-4b5e-87f6-e12c177cd823"
SECRET_KEY = "9RHCZ6BM?xZxLRmi7r7w2W4jm"

# Define file path for CSV storage
file_path = 'D:\\Downloads\\accelerometer_data1.csv'

# Buffers for storing data
data_buffer = []
plot_buffer = []

# Define buffer limit 
BUFFER_LIMIT = 10

# Variable to store the timestamp at the end of each buffer limit
buffer_end_timestamp = None

# Plotly Dash setup
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id='live-graph'),
    dcc.Interval(id='graph-update', interval=1000, n_intervals=0)
])

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
            else:
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
timestamp = None

# Helper function to update buffers and set timestamp
def update_buffers(x, y, z, ts):
    global buffer_end_timestamp
    data_buffer.append((ts, x, y, z))
    print(f"Data buffer length: {len(data_buffer)}")
    append_to_file(x, y, z)

    if len(data_buffer) >= BUFFER_LIMIT:
        plot_buffer.clear()  # Clear previous plot buffer
        plot_buffer.extend(data_buffer[:BUFFER_LIMIT])
        buffer_end_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        data_buffer.clear()  # Clear data buffer after transferring to plot buffer

# Callback function for accelerometer_X changes
def on_accelerometer_X_changed(client, value):
    global x_value
    x_value = value
    timestamp = time.time()
    print(f"accelerometer_X: {value}")
    if y_value is not None and z_value is not None:
        update_buffers(x_value, y_value, z_value, timestamp)
        x_value = None

# Callback function for accelerometer_Y changes
def on_accelerometer_Y_changed(client, value):
    global y_value
    y_value = value
    timestamp = time.time()
    print(f"accelerometer_Y: {value}")
    if x_value is not None and z_value is not None:
        update_buffers(x_value, y_value, z_value, timestamp)
        y_value = None

# Callback function for accelerometer_Z changes
def on_accelerometer_Z_changed(client, value):
    global z_value
    z_value = value
    timestamp = time.time()
    print(f"accelerometer_Z: {value}")
    if x_value is not None and y_value is not None:
        update_buffers(x_value, y_value, z_value, timestamp)
        z_value = None

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

# Helper function to format timestamp
def format_timestamp(dt):
    return dt.strftime('%d %H:%M:%S')

# Callback function to update the graph and save files
@app.callback(Output('live-graph', 'figure'), [Input('graph-update', 'n_intervals')])
def update_graph(n):
    global buffer_end_timestamp
    fig = go.Figure()
    if plot_buffer:
        timestamps, x_data, y_data, z_data = zip(*plot_buffer)
        readable_times = [datetime.fromtimestamp(ts).strftime('%M:%S') for ts in timestamps]

        # Add traces for X, Y, Z data
        fig.add_trace(go.Scatter(x=readable_times, y=x_data, mode='lines', name='X', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=readable_times, y=y_data, mode='lines', name='Y', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=readable_times, y=z_data, mode='lines', name='Z', line=dict(color='red')))         

        # Update layout
        fig.update_layout(
            title='Accelerometer Data',
            xaxis_title='Time',
            yaxis_title='Acceleration'
        )

        if buffer_end_timestamp:
            # Save the plot image with the buffer end timestamp
            image_filename = f'D:\\Downloads\\plot_{buffer_end_timestamp}.png'
            pio.write_image(fig, image_filename)

            # Save the plot data to a CSV file with the buffer end timestamp
            data_filename = f'D:\\Downloads\\data_{buffer_end_timestamp}.csv'
            with open(data_filename, 'w') as file:
                file.write("time,X,Y,Z\n")
                for i in range(len(x_data)):
                    file.write(f"{readable_times[i]},{x_data[i]},{y_data[i]},{z_data[i]}\n")

            # Reset the buffer end timestamp
            buffer_end_timestamp = None

    fig.update_layout(title='Accelerometer Data', xaxis_title='Time', yaxis_title='Acceleration')


    return fig

if __name__ == "__main__":
    # Run the Arduino Cloud client in a separate thread
    client_thread = threading.Thread(target=main)
    client_thread.start()

    # Start the Dash server
    app.run_server(debug=True)