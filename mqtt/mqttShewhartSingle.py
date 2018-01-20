import paho.mqtt.client as mqtt
import string
import random
import time


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


topic = "health"
mqttc = mqtt.Client("dimitris")
mqttc.connect("localhost", 1883)
mqttc.loop_start()
print "Connecting new Client with id:%s to the health monitor system"
print time.time();
for i in range(100):

    time.sleep(0.1);
    key =  randomword(3)
    # value = randomword(5)
    id = "dimitris"
    value = random.randint(0,100)
    if i % 20 == 0:
        value = 200000
    timestamp = int(time.time() * 1000)
    # print("%s : %d" % (key, value))
    val = str.encode(id +","+  str(value) + "," + str(timestamp))
    print val
    mqttc.publish("health_monitor/blood_pressure", val)

print "OK"
