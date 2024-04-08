from faker import Faker
import random
from datetime import datetime
import json
import subprocess

fake = Faker()

def generate_fake_record():
    vehicle_id = fake.uuid4()[:8]  # Generate a random UUID and take the first 8 characters
    vehicle_type = fake.random_element(elements=('Car', 'Truck', 'Motorcycle', 'Bus'))
    route_id = fake.random_number(digits=4)
    longitude = float(fake.longitude())  # Convert to float
    latitude = float(fake.latitude())    # Convert to float
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    speed = random.uniform(0, 120)  # Speed range assumed from 0 to 120 km/h
    fuel_level = random.uniform(0, 100)  # Fuel level range assumed from 0% to 100%

    record = {
        'vehicleId': vehicle_id,
        'vehicleType': vehicle_type,
        'routeId': route_id,
        'longitude': longitude,
        'latitude': latitude,
        'timestamp': timestamp,
        'speed': float(speed),
        'fuelLevel': float(fuel_level)
    }
    return json.dumps(record)  # Serialize the record as JSON

command = ["docker", "exec", "-i", "zookeeper-iot", "kafka-console-producer", "--broker-list", "localhost:9092", "--topic", "lambda-iot-events"]

for i in range(1, 11):
    record = generate_fake_record()
    try:
        result = subprocess.run(command, input=record, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
