import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
df = pd.read_csv('HC_SR04_data_2024-07-30_22-09-50.csv')

# Convert the Timestamp column to datetime format
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M')

# Remove ' cm' from the Distance column and convert it to numeric values
df['Distance (cm)'] = df['Distance (cm)'].str.replace(' cm', '').astype(float)

# Create a simple line plot
plt.plot(df['Timestamp'], df['Distance (cm)'], marker='o', linestyle='-', color='blue')

# Add titles and labels
plt.title('Distance Data from HC-SR04 Sensor')
plt.xlabel('Timestamp')
plt.ylabel('Distance (cm)')

# Improve layout and display the plot
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()
