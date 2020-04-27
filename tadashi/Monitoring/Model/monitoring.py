import json
import os
import time
from .counter import Counter


class Monitoring:
    def __init__(self, last_update=None, alerting=None, counters=None, last_training=None, model_size=None, model_building_time=None):
        if not last_update:
            last_counter_update = time.time()
        if not alerting:
            alerting = []
        if not counters:
            counters = []
        self._last_counter_update = last_counter_update
        self._last_training = last_training
        self._alerting = alerting
        self._metrology = counters
        self._model_size = model_size
        self._model_building_time = model_building_time

    @property
    def last_counter_update(self):
        return self._last_counter_update

    @last_counter_update.setter
    def last_counter_update(self, last_counter_update):
        self._last_counter_update = float(last_counter_update)

    @property
    def last_training(self):
        return self._last_training

    @last_training.setter
    def last_training(self, last_training):
        self._last_training = float(last_training)

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

    @property
    def model_size(self):
        return self._model_size

    @model_size.setter
    def model_size(self, model_size):
        self._model_size = model_size

    @property
    def model_building_time(self):
        return self._model_building_time

    @model_building_time.setter
    def model_building_time(self, model_building_time):
        self._model_building_time = model_building_time

    def save(self, path):
        self._last_counter_update = time.time()
        with open(path, 'w') as outfile:
            outfile.write('{\n')
            outfile.write('\t"last_counter_update" : ' + str(self._last_counter_update) + ',\n')
            if self._last_training is not None:
                outfile.write('\t"last_training" : ' + str(self._last_training) + ',\n')
            if self._model_size is not None:
                outfile.write('\t"model_size" : ' + str(self._model_size) + ',\n')
            if self._model_building_time is not None:
                outfile.write('\t"model_building_time" : "' + str(self._model_building_time) + '",\n')
            outfile.write('\t"alerting" : [\n')
            for alert in self._alerting:
                outfile.write(str(alert) + ',\n')
            outfile.write('\n],\n')
            outfile.write('\t"metrology" : [\n')
            for counter in self._metrology:
                serialized_object = counter.serialize()
                serialized_object = serialized_object.replace('_', '')
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
                if 'last_counter_update' in monitoring:
                    self._last_counter_update = monitoring['last_counter_update']
                if 'last_training' in monitoring:
                    self._last_training = monitoring['last_training']
                if 'model_size' in monitoring:
                    self._model_size = monitoring['model_size']
                if 'model_building_time' in monitoring:
                    self._model_building_time = monitoring['model_building_time']
                for alert in monitoring['alerting']:
                    self.add_alert(alert)
                for counter_object in monitoring['metrology']:
                    counter = Counter()
                    counter.unserialize(counter_object)
                    self.add_counter(counter)
