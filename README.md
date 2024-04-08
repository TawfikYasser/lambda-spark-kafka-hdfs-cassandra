# lambda-spark-kafka-hdfs-cassandra
ETL Pipeline using Lambda Architecture (Spark - Kafka - HDFS - Cassandra)

# Project Steps:

* Create a python script to generate iot data events using kafka producer.
* Pull the data using a kafka consumer then push the data to spark streaming.
* In spark streaming send and store the data in hdfs and process the data to generate stream views
and save them into cassandra.
* On the other side, in the batch layer using spark read and process the data from hdfs to generate batch views and store them into cassandra.
* Using apache superset, read the data from cassandra and build the dashboard.



# Errors and problems:

* Network issue: because I had a container for postgres with the same network range, I followed the following solution to detect the issue and fix it by removing the containers of postgres and its network:

ip addr | grep 172.22
docker network ls | grep <container-id>


* I'm using the remote development extension in vscode to connect to the containers files.
* Attach to a running container to choose the container to be used to run.
* File -> Open Folder to choose a folder inside the container to open and work in.


# Running kafka and zookeeper:

* zookeeper-server-start /etc/kafka/zookeeper.properties
* kafka-server-start /etc/kafka/server.properties
* bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sensor-data
* bin/kafka-console-producer.sh --broker-list localhost:9092 --topic sensor-data
* bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sensor-data --from-beginning


# Installing kafka inside the container:
* pip install kafka-python

# Run kafka producer from the host:

docker exec -it zookeeper-iot kafka-console-producer --broker-list localhost:9092 --topic testingKafka


# The flow will be as follows:
* On the host: use the faker lib to generate the iot events, and then using cron job to run every 10 sec to generate new data, call the docker commands to produce data to kafka.

Writing python code to call the kafka producer:

import subprocess

# Define the terminal command
```python
command = "docker exec -i zookeeper-iot kafka-console-producer --broker-list localhost:9092 --topic testingKafka"

for i in range(1, 11):
    # Run the command with 'i' as input
    result = subprocess.run(command, shell=True, input=str(i), capture_output=True, text=True)

    # Print the result
    print(result.stdout)
```

docker exec -it zookeeper-iot kafka-topics --create --zookeeper localhost:2182 --replication-factor 1 --partitions 1 
--topic lambda-iotevents



### NEW

docker exec -it zookeeper-iot kafka-topics --create --zookeeper localhost:2182 --replication-factor 1 --partitions 1 --topic test1

In the zookeeper-iot
go to /usr/bin and start kafka broker using: kafka-server-start /etc/kafka/server.properties

then use the following for consuming:
docker exec -it zookeeper-iot kafka-console-consumer --bootstrap-server localhost:9092 --topic test1 --from-beginning

and the following for producing
docker exec -it zookeeper-iot kafka-console-producer --broker-list localhost:9092 --topic test1


### SPARK STREAMING

I need to setup a consumer in spark streaming to read the data from the kafka topic, process the data to produce real-time view and save them in cassandra.

Also, it should store the data in hdfs for further batch processing using spark to produce batch views to be saved in cassandra.


In the spark master container:

To run the spark-consumer in the container:

./spark-submit --package org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 /home/spark-streaming-consumer.py

Now the script saves the data in a file in /home/data

we need to update it to write the data to HDFS, and also apply any simple transformation then write the updated data to cassandra.

Now data is moved from the spark-streaming to hdfs successfully!


-------------------------------------------

Now we need to apply a simple transformatin to group by vehicle type and do avg of speed and save the result df to cassandra.

log in to casssandra:

cqlsh --username cassandra --password cassandra




then I want to do the following:

Airflow: To run the kafka-producer every 1 minute
Airflow: To run the spark-batch-processor every 1 minute on the data in hdfs
