import subprocess

command = ["docker", "exec", "-i", "zookeeper-iot", "kafka-console-consumer", "--bootstrap-server", "localhost:9092", "--topic", "test1", "--from-beginning"]

try:
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for line in process.stdout:
        print(line.strip())  # Print each line of output from the consumer
    process.communicate()  # Wait for the process to finish
except Exception as e:
    print(f"Error: {e}")

