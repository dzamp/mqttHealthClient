import string
import random
import time
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


producer = KafkaProducer(bootstrap_servers=['195.134.67.223:9092'])
topic = "testnifi"

for i in range(10000):
    key =  randomword(3)
    # value = randomword(5)
    time.sleep(1)
    value = random.randint(1,100);
    print("%s : %d" % (key, value))
    producer.send(topic,key = str.encode(key),  value = str.encode(str(value)))

print "OK"




# #Zookeeper
# sudo ./zkServer.sh start
#
# #Kafka server
# sudo ./kafka-server-start.sh ../config/server.properties
#
# #Kafka topic creation
# bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic Hello-Kafka
#
# #See more here
# https://www.tutorialspoint.com/apache_kafka/apache_kafka_basic_operations.htm
