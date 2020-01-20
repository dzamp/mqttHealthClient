#!/usr/bin/python2.7
import sys
import json
# import numpy as np
# import pandas as pd

class RandomKV:
    def __init__(self,timestamp,value):
        self.key = timestamp
        self.value = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


flowfile = sys.stdin.read()
print flowfile
# exampleFlowfile= json.loads(flowfile)

alert = RandomKV("hey",flowfile[0])
sys.stdout.write("{2}\n".format(alert.toJSON()))
# sys.stdout.write(str(flowfile))
