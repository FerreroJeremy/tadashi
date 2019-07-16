import json


class Device:
    def __init__(self, id=None, name=None, roomID=None, type=None, baseType=None, value=None, batteryLevel=None, dead=None, timestamp=None):
        self._id = id
        self._name = name
        self._roomID = roomID
        self._type = type
        self._baseType = baseType
        self._value = value
        self._batteryLevel = batteryLevel
        self._dead = dead
        self._timestamp = timestamp

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def roomID(self):
        return self._roomID

    @roomID.setter
    def roomID(self, roomID):
        self._roomID = roomID

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def baseType(self):
        return self._baseType

    @baseType.setter
    def baseType(self, baseType):
        self._baseType = baseType

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def batteryLevel(self):
        return self._batteryLevel

    @batteryLevel.setter
    def batteryLevel(self, batteryLevel):
        self._batteryLevel = batteryLevel

    @property
    def dead(self):
        return self._dead

    @dead.setter
    def dead(self, dead):
        self._dead = dead

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    def serialize(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

    def unserialize(self, dict_object):    
        self.id = dict_object['id']
        self.name = dict_object['name']
        self.roomID = dict_object['roomID']
        self.type = dict_object['type']
        self.baseType = dict_object['baseType']
        self.value = dict_object['value']
        self.batteryLevel = dict_object['batteryLevel']
        self.dead = dict_object['dead']
        self.timestamp = dict_object['timestamp']

