# from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json
# from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# # Create a SparkSession
# spark = SparkSession.builder \
#     .appName("KafkaReader") \
#     .getOrCreate()

# # Define the Kafka topic to read from
# kafka_topic = "lambda-iot-events"

# # Define the Kafka broker endpoint
# kafka_bootstrap_servers = "172.23.0.2:9092"

# # Define the schema for the JSON records
# schema = StructType([
#     StructField("vehicleId", StringType(), nullable=False),
#     StructField("vehicleType", StringType(), nullable=False),
#     StructField("routeId", IntegerType(), nullable=False),
#     StructField("longitude", DoubleType(), nullable=False),
#     StructField("latitude", DoubleType(), nullable=False),
#     StructField("timestamp", TimestampType(), nullable=False),
#     StructField("speed", DoubleType(), nullable=False),
#     StructField("fuelLevel", DoubleType(), nullable=False)
# ])

# # Read data from Kafka using Spark
# kafka_df = spark \
#     .readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
#     .option("subscribe", kafka_topic) \
#     .option("startingOffsets", "latest")\
#     .load()

# # Parse the value column as JSON using the defined schema
# parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
#     .select(from_json("value", schema).alias("data")) \
#     .select("data.*")

# # # Start the streaming query
# # query = parsed_df \
# #     .writeStream \
# #     .outputMode("append") \
# #     .format("console") \
# #     .start()

# # Start the streaming query to write results as CSV
# query = parsed_df \
#     .writeStream \
#     .outputMode("append") \
#     .format("csv") \
#     .option("path", "/home/data") \
#     .option("checkpointLocation", "/home/checkpoint") \
#     .start()

# # Wait for the termination of the query
# query.awaitTermination()


from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, avg
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType

# Import Cassandra connector
from pyspark.sql.streaming import DataStreamWriter

# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaReader") \
    .config("spark.cassandra.connection.host", "172.23.0.6") \
    .config("spark.driver.extraClassPath", "/home/spark-cassandra-connector_2.12-3.0.0.jar") \
    .getOrCreate()

# Define the Kafka topic to read from
kafka_topic = "lambda-iot-events"

# Define the Kafka broker endpoint
kafka_bootstrap_servers = "172.23.0.2:9092"

# Define the schema for the JSON records
schema = StructType([
    StructField("vehicleId", StringType(), nullable=False),
    StructField("vehicleType", StringType(), nullable=False),
    StructField("routeId", IntegerType(), nullable=False),
    StructField("longitude", DoubleType(), nullable=False),
    StructField("latitude", DoubleType(), nullable=False),
    StructField("timestamp", TimestampType(), nullable=False),
    StructField("speed", DoubleType(), nullable=False),
    StructField("fuelLevel", DoubleType(), nullable=False)
])

# Read data from Kafka using Spark
kafka_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "latest") \
    .load()

# Parse the value column as JSON using the defined schema
parsed_df = kafka_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", schema).alias("data")) \
    .select("data.*")

# Apply transformations on the data (speed views to cassandra)
grouped_df = parsed_df.groupBy("vehicleType").agg(avg("speed").alias("avg_speed"))

# Write transformed data to Cassandra
# cassandra_query = grouped_df \
#     .writeStream \
#     .foreachBatch(lambda batch_df, batch_id: batch_df.write \
#         .format("org.apache.spark.sql.cassandra") \
#         .options(table="speed", keyspace="iot_events") \
#         .mode("append") \
#         .save()) \
#     .outputMode("update") \
#     .start()

# # Wait for the termination of the query
# cassandra_query.awaitTermination()

# Write transformed data to HDFS
query = parsed_df \
    .writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "hdfs://namenode:8020/iot-events/batchData") \
    .option("checkpointLocation", "/home/checkpoint") \
    .start()

# Wait for the termination of the query
query.awaitTermination()
