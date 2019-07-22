import json
import os
import time
from .device import Device


class History:
    def __init__(self, timestamp=None, logs=None):
        if not logs:
            logs = []
        if not timestamp:
            timestamp = time.time()
        self._timestamp = timestamp
        self._logs = logs

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = float(timestamp)

    @property
    def logs(self):
        return self._logs

    def add_log(self, log):
        self._logs.append(log)

    def save(self, path):
        with open(path, 'w') as outfile:
            outfile.write('{\n')
            outfile.write('\t"timestamp" : ' + str(self._timestamp) + ',\n')
            outfile.write('\t"logs" : [\n')
            for log in self._logs:
                serialized_object = log.serialize()
                serialized_object = serialized_object.replace('_', '')
                outfile.write(serialized_object)
                outfile.write(',\n')
            outfile.seek(outfile.tell() - 2, os.SEEK_SET)
            outfile.truncate()
            outfile.write('\n]\n')
            outfile.write('\n}\n')

    def load(self, path):
        with open(path) as json_file:
            history = json.load(json_file)
            self.timestamp = history['timestamp']
            for _oject in history['logs']:
                log = Device()
                log.unserialize(_oject)
                self.add_log(log)
