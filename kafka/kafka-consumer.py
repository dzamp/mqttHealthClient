from kafka import KafkaConsumer


topic = 'hello'
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         auto_offset_reset='earliest',
                         consumer_timeout_ms=1000)
consumer.subscribe([topic])
for message in consumer:
    print("new message Arrived!\n" + str(message))