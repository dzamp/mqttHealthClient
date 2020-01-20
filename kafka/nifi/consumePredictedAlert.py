from kafka import KafkaConsumer
import csv
import json

class Alert:
    def __init__(self,prediction_time,predicted_value, timestamp,value):
        self.prediction_time = prediction_time
        self.predicted_value = predicted_value
        self.timestamp = timestamp
        self.value = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)



topic = 'testnifi_predict'
consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                         auto_offset_reset='latest',
                         consumer_timeout_ms=1000000)

alerts = []
consumer.subscribe([topic])
for message in consumer:
    why = message.value.split(',')
    al = Alert(why[0],why[1],why[2],why[3])
    print ("%s,%s,%s,%s" % (al.prediction_time,al.predicted_value,al.timestamp,al.value))
    with open('temperature_prediction_change.csv', mode='a+') as temperature_file:
        temperature_writer = csv.writer(temperature_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        temperature_writer.writerow([al.prediction_time, al.predicted_value,al.timestamp,al.value])
