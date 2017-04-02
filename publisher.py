import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("test.mosquitto.org", 1883)
mqttc.publish("blood_pressure", "Hello, World!")
mqttc.loop(2) #timeout = 2s

