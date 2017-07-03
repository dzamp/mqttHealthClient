#!/usr/bin/env python

from threading import Thread, Event
import argparse
import time, datetime
import random
import json
import paho.mqtt.client as mqtt


class Client(Thread):
    percentage = 20
    time_units = 20
    quick_scale = 0
    time_inerval = 0.5
    measurements_per_minute = 10
    sleep_interval = 6
    values = []
    mqttc = mqtt.Client("python_pub")
    mqttc.connect("localhost", 1883)

    def __init__(self, measurements_per_minute, event, client_id,quick_scale, host, port, client_name):
        super(Client, self).__init__()
        self._stop = event
        self.measurements_per_minute = measurements_per_minute
        self.sleep_interval =  60/float(self.measurements_per_minute)
        self.client_id = client_id
        self.quick_scale = quick_scale
        self.mqttc = mqtt.Client(client_name)
        self.mqttc.connect(host, port)
        print "Constructing client with measurements_per_minute %d  sleep interval  %d" % (measurements_per_minute,self.sleep_interval)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        # timeout = 20s
        self.mqttc.loop_start()
        self.prepare()
        print self.values
        print "Connecting new Client with id:%s to the health monitor system" %self.client_id
        self.mqttc.publish("health_monitor/subscribe_client", self.client_id)
        time.sleep(3)
        if self.quick_scale==1:
            self.simulate_quick_scale();
            return None
        length = len(self.values)
        counter = 0
        pos=0
        print "sleep interval %f" % (60/float(self.measurements_per_minute))
        while not self.stopped():
            if counter >= self.measurements_per_minute:
                counter = 0
                pos += 1
                if pos >= length:
                    pos = 0
                    print "==========================================="
            counter += 1
            self.emit(round(random.uniform(self.values[pos]-0.5, self.values[pos]+0.5),1))
            time.sleep(self.sleep_interval)

    def simulate_quick_scale(self):
        for i in range(0,9):
            time.sleep(1)
            rounded_number = round(random.uniform(0.1, 0.5), 1)
            self.emit(self.values[i] + rounded_number)

    def emit(self, value):
        timestamp =  int(time.time() * 1000)
        data = self.client_id+ ","+ str(value) + "," + str(int(time.time() * 1000))
        self.mqttc.publish("health_monitor/temperature", data)
        print "Emiting values " + data
        #replace print with actual communication method
        # print data


    def prepare(self):
        # simulate a normal distribution of values sorted
        self.values.append(round(random.uniform(36.6, 37.0), 1))
        self.values.append(round(random.uniform(37.0, 37.5), 1))
        self.values.append(round(random.uniform(37.5, 38.0), 1))
        self.values.append(round(random.uniform(38.0, 38.5), 1))
        self.values.append(round(random.uniform(38.5, 38.8), 1))
        self.values.append(round(random.uniform(38.8, 39.0), 1))
        self.values.append(round(random.uniform(39.0, 38.0), 1))
        self.values.append(round(random.uniform(38.0, 37.0), 1))
        self.values.append(round(random.uniform(37.0, 36.6), 1))

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('measurements_per_minute', type=int,
                        help='how many measurements per minute')
    parser.add_argument('client_id', type=str,
                        help='the client id connecting')
    parser.add_argument('quick_scale', type=int,
                        help='simulate quick pressure change')
    parser.add_argument('host', type=str,
                                    help='Host ip  for the mosquitto broker')
    parser.add_argument('port', type=int,
                        help='post for the mosquitto broker')
    parser.add_argument('mosquitto_client_name', type=str,
                        help='name of the mosquitto client')
    args = parser.parse_args()
    stop_event = Event()
    client = Client(args.measurements_per_minute, stop_event, args.client_id, args.quick_scale, args.host, args.port, args.mosquitto_client_name)
    client.start()
    try:
        while 1:
            time.sleep(.01)
    except KeyboardInterrupt:
        stop_event.set()
        client.join()
        print "Client successfully terminated"


if __name__ == '__main__':
    main()
