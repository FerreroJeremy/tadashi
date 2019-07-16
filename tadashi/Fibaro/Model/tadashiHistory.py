import json
import os
from enum import Enum
from .history import History
from .room import Room
from ..Exception.badArgumentTypeException import BadArgumentTypeException


class Context(Enum):
    SHOWERING = 'shower'
    WORKING = 'briefcase'
    SLEEPING = 'bed'
    PLAYING = 'gamepad'
    GARDENING = 'leaf'
    TRAVELING = 'plane'
    UNKNOWN = 'adjust'


class TadashiHistory(History):
    def __init__(self, timestamp=None, context=None, logs=None):
        super().__init__()
        self._context = context

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        if isinstance(context, str):
            context = Context[context]
        
        if not isinstance(context, Context):
            raise BadArgumentTypeException('context must be an instance of Context Enum')
        self._context = context

    def save(self, path):
        with open(path, 'w') as outfile:
            outfile.write('{\n')
            outfile.write('\t"timestamp" : ' + str(self._timestamp) + ',\n')
            if self._context is not None:
                outfile.write('\t"context" : "' + str(self._context.name) + '",\n')
            outfile.write('\t"logs" : [\n')
            for log in self._logs:
                serialized_object = log.serialize()
                serialized_object = serialized_object.replace('_','')
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
            if 'context' in history:
                self.context = history['context']
            for oject in history['logs']:
                log = Room()
                log.unserialize(oject)
                self.add_log(log)

