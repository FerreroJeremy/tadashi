import json


class Counter:
    def __init__(self, _id=None, room_id=None, _type=None, base_type=None, value=None, count=None, corrected=None):
        self._id = _id
        self._roomID = room_id
        self._type = _type
        self._baseType = base_type
        self._value = value
        self._count = count
        self._corrected = corrected

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id):
        self._id = _id

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
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._count = count

    @property
    def corrected(self):
        return self._corrected

    @corrected.setter
    def corrected(self, corrected):
        self._corrected = corrected

    def serialize(self):
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

    def unserialize(self, dict_object):
        self.id = dict_object['id']
        self.roomID = dict_object['roomID']
        self.type = dict_object['type']
        self.baseType = dict_object['baseType']
        self.value = dict_object['value']
        self.count = dict_object['count']
        self.corrected = dict_object['corrected']
