#!/usr/bin/env python

from threading import Thread, Event
import argparse
import time, datetime
import random
import json
import paho.mqtt.client as mqtt


class Client(Thread):
    percentage = 20
    quick_scale = 0
    time_units = 20
    time_inerval = 0.5
    client_id = 1
    sleep_interval = 6
    values = []

    # OLD def __init__(self, measurements_per_minute, event, client_id, quick_scale, host, port, client_name):
    def __init__(self, client_id, host, port, client_name):
        super(Client, self).__init__()
        # self._stop = event
        self.client_id = client_id
        self.mqttc = mqtt.Client(client_name)
        self.mqttc.connect(host, port)
        # print "Constructing client with measurements_per_minute %d  sleep interval  %f" % (measurements_per_minute,self.sleep_interval)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        # timeout = 20s
        self.mqttc.loop_start()
        print "Connecting new Client with id:%s to the health monitor system" %self.client_id
        # self.mqttc.publish("health_monitor/subscribe_client", self.client_id)
        time.sleep(3)
        while True :
            self.emitValues()

    def emitValues(self):
        for i in range(0,10):
            self.emit(random.randint(0,9000))
            time.sleep(0.5)


    def emit(self, value):
        timestamp =  int(time.time() * 1000)
        data = str(value)
        self.mqttc.publish("health_monitor/blood_pressure", data)
        print "Emiting values " + data
        #replace print with actual communication method
        # print data


    # r = randint(0,9)
    # print r
def main():
    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('client_id', type=str,
                        help='the client id connecting')
    # parser.add_argument('quick_scale', type=int,
    #                     help='simulate quick pressure change')
    parser.add_argument('host', type=str,
                                    help='Host ip  for the mosquitto broker')
    parser.add_argument('port', type=int,
                        help='post for the mosquitto broker')
    parser.add_argument('mosquitto_client_name', type=str,
                        help='name of the mosquitto client')
    args = parser.parse_args()
    # old stop_event = Event()
    client = Client( args.client_id, args.host, args.port, args.mosquitto_client_name)
    # old client = Client(args.measurements_per_minute, stop_event, args.client_id, args.quick_scale, args.host, args.port, args.mosquitto_client_name)
    client.start()
    # try:
    #     while 1:
    #         time.sleep(.01)
    # except KeyboardInterrupt:
    #     stop_event.set()
    #     client.join()
    #     print "Client successfully terminated"


if __name__ == '__main__':
    main()
