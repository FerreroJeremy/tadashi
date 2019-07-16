import json
import os
import time
from .counter import Counter

class Monitoring:
    def __init__(self, last_update=None, alerting=None, counters=None):
        if not last_update:
            last_update = time.time()
        if not alerting:
            alerting = []
        if not counters:
            counters = []
        self._last_update = last_update
        self._alerting = alerting
        self._metrology = counters

    @property
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, last_update):
        self._last_update = float(last_update)

    @property
    def alerting(self):
        return self._alerting

    def add_alert(self, alert):
        self._alerting.append(alert)

    @property
    def metrology(self):
        return self._metrology

    def add_counter(self, counter):
        self._metrology.append(counter)

    def save(self, path):
        with open(path, 'w') as outfile:
            outfile.write('{\n')
            outfile.write('\t"last_update" : ' + str(self._last_update) + ',\n')
            outfile.write('\t"alerting" : [\n')
            for alert in self._alerting:
                outfile.write(str(alert) + ',\n')
            outfile.write('\n],\n')
            outfile.write('\t"metrology" : [\n')
            for counter in self._metrology:
                serialized_object = counter.serialize()
                serialized_object = serialized_object.replace('_','')
                outfile.write(serialized_object)
                outfile.write(',\n')
            outfile.seek(outfile.tell() - 2, os.SEEK_SET)
            outfile.truncate()
            outfile.write('\n]\n')
            outfile.write('\n}\n')

    def load(self, path):
        if os.path.isfile(path):
            with open(path) as json_file:
                monitoring = json.load(json_file)
                self.last_update = monitoring['last_update']
                for alert in monitoring['alerting']:
                    self.add_alert(alert)
                for object in monitoring['metrology']:
                    counter = Counter()
                    counter.unserialize(object)
                    self.add_counter(counter)

