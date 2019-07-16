import json


class Counter:
    def __init__(self, id=None, roomID=None, type=None, baseType=None, value=None, count=None, corrected=None):
        self._id = id
        self._roomID = roomID
        self._type = type
        self._baseType = baseType
        self._value = value
        self._count = count
        self._corrected = corrected

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

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

