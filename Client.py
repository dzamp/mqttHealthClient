#!/usr/bin/env python

from threading import Thread, Event
import argparse
import time
import random
import json
import paho.mqtt.client as mqtt


class Client(Thread):
    percentage = 20
    time_units = 20
    time_inerval = 0.5
    measurements_per_minute = 10
    sleep_interval = 6
    values = []
    mqttc = mqtt.Client("python_pub")
    mqttc.connect("workstation00.raspberryip.com", 1883)
    class Tuple:
        patient_id = "0"
        measurement = 0
        def __init__(self, p, m):
            self.measurement = m
            self.patient_id = p

    def __init__(self, measurements_per_minute, event):
        super(Client, self).__init__()
        self._stop = event
        self.measurements_per_minute = measurements_per_minute
        self.sleep_interval =  int(60/self.measurements_per_minute)

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
        length = len(self.values)
        counter = 0
        pos=0
        print "sleep interval %d" % int(60/self.measurements_per_minute)
        while not self.stopped():
            if counter >= self.measurements_per_minute:
                counter = 0
                pos += 1
                if pos >= length:
                    pos = 0
                    print "==========================================="
            counter += 1
            self.emit(self.values[pos])
            time.sleep(self.sleep_interval)



    def emit(self, value):
        tuple = self.Tuple("01",value)
        data = json.dumps(tuple.__dict__)
        self.mqttc.publish("blood_pressure", data)
        print "Emiting values " + data
        #replace print with actual communication method
        # print data


    def prepare(self):
        # simulate a normal distribution of values sorted
        self.values.append(random.randint(80, 85))
        self.values.append(random.randint(90, 95))
        self.values.append(random.randint(96, 100))
        self.values.append(random.randint(105, 121))
        self.values.append(random.randint(130, 141))
        self.values.append(random.randint(105, 121))
        self.values.append(random.randint(96, 100))
        self.values.append(random.randint(90, 95))
        self.values.append(random.randint(80, 85))
    # r = randint(0,9)
    # print r
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('measurements_per_minute', type=int,
                        help='how many measurements per minute')
    args = parser.parse_args()
    stop_event = Event()
    client = Client(args.measurements_per_minute, stop_event)
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
