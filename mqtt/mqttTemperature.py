import paho.mqtt.client as mqtt
import string
import random
import time


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def prepare():
    values = []
    # simulate a normal distribution of values sorted
    values.append(round(random.uniform(36.6, 37.0), 1))
    values.append(round(random.uniform(37.0, 37.5), 1))
    values.append(round(random.uniform(37.5, 38.0), 1))
    values.append(round(random.uniform(38.0, 38.5), 1))
    values.append(round(random.uniform(38.5, 38.8), 1))
    values.append(round(random.uniform(38.8, 39.0), 1))
    values.append(round(random.uniform(39.0, 40.0), 1))
    values.append(round(random.uniform(39.0, 38.0), 1))
    values.append(round(random.uniform(38.0, 37.0), 1))
    values.append(round(random.uniform(37.0, 36.6), 1))
    return values

def emit(value):
    timestamp = int(time.time() * 1000)
    data = "dimitris" + "," + str(value) + "," + str(int(time.time() * 1000))
    mqttc.publish(topic, data)
    print "Emiting values " + data

topic = "temperature"
mqttc = mqtt.Client("dimitris")
mqttc.connect("localhost", 1883)
mqttc.loop_start()
print "Connecting new Client with id:%s to the health monitor system"
print time.time();
values = prepare()
pos = 0;
count =0
for i in range(10):
    emit(round(random.uniform(values[pos] - 0.5, values[pos] + 0.5), 1))
    time.sleep(0.5)
    if (i != 0 and i % 10 == 0):
        pos = pos + 1;

    count+=1
print "OK " + str(count)


