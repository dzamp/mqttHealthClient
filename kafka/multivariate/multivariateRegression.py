from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import cm
import json
import string
import random
import time
import math
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import csv

class Alert:
    def __init__(self,timestamp,value,independentVariable):
        self.timestamp = timestamp
        self.value = value
        self.x = independentVariable

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)



def generateTemp(initialValue, slope, time, slope2, independentVar):
    return initialValue + random.randrange(-1,1) + round(slope * time) + slope2*independentVar




isrunning = 1
host = 'localhost'
producer = KafkaProducer(bootstrap_servers=[host+':9092'])

topic = "testnifi"
start_time = int(1000 * time.time())
alerts = []
# newMap = {"key":"ffff"}
# for k, v in vars().items():
#     if not (k.startswith('__') and k.endswith('__')):
#         newMap[k] = v



for i in range(1, 10000):
    currTime = int(1000*time.time())
    antigoni = Alert(currTime, generateTemp(10, +0.0003, currTime-start_time, 0.0002, i),i)
    time.sleep(0.01)
    print( antigoni.toJSON())
    producer.send("testnifi", antigoni.toJSON())
    alerts.append(antigoni)

with open('multivariate_log.csv', mode='w') as temperature_file:
    temperature_writer = csv.writer(temperature_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in alerts:
        temperature_writer.writerow([row.timestamp, row.value, row.x])
