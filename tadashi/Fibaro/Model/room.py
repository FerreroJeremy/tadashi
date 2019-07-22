import json
from enum import Enum
from ..Exception.badArgumentTypeException import BadArgumentTypeException


class OpeningState(Enum):
    OPEN = 1
    CLOSE = 0


class MonoxideState(Enum):
    SAFE = 0
    MODERATE = 1
    DANGEROUS = 2


class Place(Enum):
    LOUNGE = 1
    BEDROOM = 2
    BATHROOM = 3
    OUTSIDE = 4


class Room:
    def __init__(
            self,
            place=Place.LOUNGE,
            light=False,
            temperature=None,
            motion=False,
            humidity=False,
            gaz=MonoxideState.SAFE,
            door=OpeningState.CLOSE,
            shutter=OpeningState.CLOSE,
            noise=False,
            vaccum=False
    ):
        if not isinstance(place, Place):
            raise BadArgumentTypeException('place must be an instance of Place Enum')

        if not isinstance(light, bool):
            raise BadArgumentTypeException('light must be a bool')

        if not isinstance(temperature, float):
            self._temperature = None
        else:
            self._temperature = temperature

        if not isinstance(motion, bool):
            raise BadArgumentTypeException('motion must be a bool')

        if not isinstance(humidity, bool):
            raise BadArgumentTypeException('humidity must be a bool')

        if not isinstance(noise, bool):
            raise BadArgumentTypeException('noise must be a bool')

        if not isinstance(vaccum, bool):
            raise BadArgumentTypeException('vaccum must be a bool')

        self._place = place
        self._light = light
        self._motion = motion
        self._humidity = humidity
        self._light = light
        self.gaz = gaz
        self.door = door
        self.shutter = shutter
        self._noise = noise
        self._vaccum = vaccum

    @property
    def place(self):
        return self._place

    @property
    def light(self):
        return self._light

    @property
    def temperature(self):
        return self._temperature

    @property
    def motion(self):
        return self._motion

    @property
    def humidity(self):
        return self._humidity

    @property
    def gaz(self):
        return self._gaz

    @property
    def door(self):
        return self._door

    @property
    def shutter(self):
        return self._shutter

    @property
    def noise(self):
        return self._noise

    @property
    def vaccum(self):
        return self._vaccum

    @place.setter
    def place(self, place):
        if isinstance(place, int):
            place = Place(place)

        if not isinstance(place, Place):
            raise BadArgumentTypeException('place must be an instance of Place Enum')
        self._place = place

    @light.setter
    def light(self, light):
        if not isinstance(light, bool):
            raise BadArgumentTypeException('light must be a bool')
        self._light = light

    @temperature.setter
    def temperature(self, temperature):
        if temperature is not None:
            self._temperature = float(temperature)
        else:
            self._temperature = None

    @motion.setter
    def motion(self, motion):
        if not isinstance(motion, bool):
            raise BadArgumentTypeException('motion must be a bool')
        self._motion = motion

    @humidity.setter
    def humidity(self, humidity):
        if not isinstance(humidity, bool):
            raise BadArgumentTypeException('humidity must be a bool')
        self._humidity = humidity

    @gaz.setter
    def gaz(self, gaz):
        if isinstance(gaz, int):
            gaz = MonoxideState(gaz)
        if not isinstance(gaz, MonoxideState):
            raise BadArgumentTypeException('gaz must be an instance of MonoxideState Enum')
        self._gaz = gaz

    @door.setter
    def door(self, door):
        if isinstance(door, int):
            door = OpeningState(door)
        if not isinstance(door, OpeningState):
            raise BadArgumentTypeException('door must be an instance of OpeningState Enum')
        self._door = door

    @shutter.setter
    def shutter(self, shutter):
        if isinstance(shutter, int):
            shutter = OpeningState(shutter)
        if not isinstance(shutter, OpeningState):
            raise BadArgumentTypeException('shutter must be an instance of OpeningState Enum')
        self._shutter = shutter

    @noise.setter
    def noise(self, noise):
        if not isinstance(noise, bool):
            raise BadArgumentTypeException('noise must be a bool')
        self._noise = noise

    @vaccum.setter
    def vaccum(self, vaccum):
        if not isinstance(vaccum, bool):
            raise BadArgumentTypeException('vaccum must be a bool')
        self._vaccum = vaccum

    def serialize(self):
        self._place = int(self._place.value)
        self._gaz = int(self._gaz.value)
        self._door = int(self._door.value)
        self._shutter = int(self._shutter.value)
        return json.dumps(self.__dict__, indent=4, ensure_ascii=False)

    def unserialize(self, dict_object):
        self.place = dict_object['place']
        self.light = dict_object['light']
        self.temperature = dict_object['temperature']
        self.motion = dict_object['motion']
        self.humidity = dict_object['humidity']
        self.gaz = dict_object['gaz']
        self.door = dict_object['door']
        self.shutter = dict_object['shutter']
        self.noise = dict_object['noise']
        self.vaccum = dict_object['vaccum']
