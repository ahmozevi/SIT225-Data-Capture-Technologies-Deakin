import pandas as pd
import matplotlib.pyplot as plt

# Load temperature data
temperature_data = pd.read_csv('DHT_22-temperature.csv')

# Convert 'time' column to datetime
temperature_data['time'] = pd.to_datetime(temperature_data['time'])

# Plot Temperature
plt.figure(figsize=(12, 6))

# Plot temperature
plt.plot(temperature_data['time'], temperature_data['value'], label='Temperature', color='tab:orange')
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('Temperature Over Time')
plt.legend()
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
