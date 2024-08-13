import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the CSV File
df = pd.read_csv('gyroscope_data.csv')  # Load the CSV file into a DataFrame

# Step 2: Group by 'timestamp' and aggregate the X, Y, Z values by taking the mean
df_grouped = df.groupby('timestamp').agg({
    'X': 'mean',  # Compute the average X value for each timestamp
    'Y': 'mean',  # Compute the average Y value for each timestamp
    'Z': 'mean'   # Compute the average Z value for each timestamp
}).reset_index()  # Reset index to make 'timestamp' a column again

# Step 3: Plot the data

# Plot all three variables together
plt.figure(figsize=(12, 6))  # Create a figure with specified size
plt.plot(df_grouped['timestamp'], df_grouped['X'], label='X', color='r')  # Plot X values
plt.plot(df_grouped['timestamp'], df_grouped['Y'], label='Y', color='g')  # Plot Y values
plt.plot(df_grouped['timestamp'], df_grouped['Z'], label='Z', color='b')  # Plot Z values
plt.xlabel('Timestamp')  # Label for the x-axis
plt.ylabel('Value')      # Label for the y-axis
plt.title('Gyroscope X, Y, Z values')  # Title of the plot
plt.legend()             # Show the legend to identify lines

# Rotate x-axis labels and adjust layout
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels to make them readable

# Reduce the number of x-axis labels
num_labels = len(df_grouped['timestamp'])  # Get the total number of labels
step = max(1, num_labels // 10)  # Determine step size to reduce the number of labels
plt.xticks(df_grouped['timestamp'][::step])  # Set x-axis ticks to show fewer labels

plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.show()  # Display the plot
