import pandas as pd
import matplotlib.pyplot as plt

# Load and prepare humidity data
humidity_data = pd.read_csv('DHT_22-humidity.csv')
humidity_data['time'] = pd.to_datetime(humidity_data['time'])

# Load and prepare temperature data
temperature_data = pd.read_csv('DHT_22-temperature.csv')
temperature_data['time'] = pd.to_datetime(temperature_data['time'])

# Create a combined plot
plt.figure(figsize=(12, 6))

# Plot temperature data
plt.plot(temperature_data['time'], temperature_data['value'], label='Temperature', color='tab:blue')

# Plot humidity data
plt.plot(humidity_data['time'], humidity_data['value'], label='Humidity', color='tab:green')

# Add labels and title
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Temperature and Humidity Over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('combined_plot.png')  # Save the combined plot
plt.show()
