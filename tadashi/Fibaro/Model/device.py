import json


class Device:
    def __init__(self, _id=None, name=None, room_id=None, _type=None, base_type=None, value=None, battery_level=None, dead=None, timestamp=None):
        self._id = _id
        self._name = name
        self._roomID = room_id
        self._type = _type
        self._baseType = base_type
        self._value = value
        self._batteryLevel = battery_level
        self._dead = dead
        self._timestamp = timestamp

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

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
    def roomID(self, room_id):
        self._roomID = room_id

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._type = _type

    @property
    def baseType(self):
        return self._baseType

    @baseType.setter
    def baseType(self, base_type):
        self._baseType = base_type

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
    def batteryLevel(self, battery_level):
        self._batteryLevel = battery_level

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
