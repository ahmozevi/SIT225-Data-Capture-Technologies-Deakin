import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import csv

# Initialize Firebase
cred = credentials.Certificate('D:key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bookstoreproject-9b273-default-rtdb.firebaseio.com/'
})

# Reference to Firebase database
ref = db.reference('/gyroscope_data')

# Get data from Firebase
data = ref.get()

# Save data to a CSV file
with open('gyroscope_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['timestamp', 'X', 'Y', 'Z']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for key, value in data.items():
        writer.writerow({
            'timestamp': value['timestamp'],  # Use the timestamp directly
            'X': value['X'],
            'Y': value['Y'],
            'Z': value['Z']
        })

print("Data saved to gyroscope_data.csv")
