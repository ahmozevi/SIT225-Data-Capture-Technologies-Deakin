import pandas as pd
import matplotlib.pyplot as plt

# Load humidity data
humidity_data = pd.read_csv('DHT_22-humidity.csv')

# Convert 'time' column to datetime
humidity_data['time'] = pd.to_datetime(humidity_data['time'])

# Plot Humidity
plt.figure(figsize=(12, 6))

# Plot humidity
plt.plot(humidity_data['time'], humidity_data['value'], label='Humidity', color='tab:blue')
plt.xlabel('Time')
plt.ylabel('Humidity (%)')
plt.title('Humidity Over Time')
plt.legend()
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
