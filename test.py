import subprocess
# from faker import Faker
# import random
# from datetime import datetime
# import json

# fake = Faker()

# def generate_fake_record():
#     vehicle_id = fake.uuid4()[:8]  # Generate a random UUID and take the first 8 characters
#     vehicle_type = fake.random_element(elements=('Car', 'Truck', 'Motorcycle', 'Bus'))
#     route_id = fake.random_number(digits=4)
#     longitude = float(fake.longitude())  # Convert to float
#     latitude = float(fake.latitude())    # Convert to float
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     speed = random.uniform(0, 120)  # Speed range assumed from 0 to 120 km/h
#     fuel_level = random.uniform(0, 100)  # Fuel level range assumed from 0% to 100%

#     record = {
#         'vehicleId': vehicle_id,
#         'vehicleType': vehicle_type,
#         'routeId': route_id,
#         'longitude': longitude,
#         'latitude': latitude,
#         'timestamp': timestamp,
#         'speed': float(speed),
#         'fuelLevel': float(fuel_level)
#     }
#     return record

# command = "docker exec -i zookeeper-iot kafka-console-producer --broker-list localhost:9092 --topic lambda-iotevents"

# for i in range(1, 11):
#     # Generate a fake record
#     record = generate_fake_record()

#     # Serialize the record object to JSON string
#     json_string = json.dumps(record)

#     # Construct the command
#     subprocess.run(f"echo '{json_string}' | {command}", shell=True)


command = "docker exec -it zookeeper-iot kafka-console-producer --broker-list localhost:9092 --topic testingKafka"

for i in range(1, 11):
    # Run the command with 'i' as input
    result = subprocess.run(command, shell=True, input=str(i), capture_output=True, text=True)

    # Print the result
    print(result.stdout)