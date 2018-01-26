import paho.mqtt.client as mqtt
import string
import random
import time


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


topic = "health_monitor/blood_pressure"
mqttc = mqtt.Client("dimitris")
mqttc.connect("localhost", 1883)
mqttc.loop_start()
print "Connecting new Client with id:%s to the health monitor system"
print time.time();
count = 0;

for i in range(10):

    time.sleep(0.5);
    key =  randomword(3)
    # value = randomword(5)
    id = "dimitris"
    value = random.randint(0,10)
    # if i % 199 == 0:
    #     value = 200000
    timestamp = int(time.time() * 1000)
    # print("%s : %d" % (key, value))
    val = str.encode(id +","+  str(value) + "," + str(timestamp))
    print val
    mqttc.publish(topic, val)
    count+=1
print "OK " + str(count)
