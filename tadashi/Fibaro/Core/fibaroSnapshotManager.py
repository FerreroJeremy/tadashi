import os
import json
from enum import Enum
from ..Api.fibaroApiWrapper import FibaroApiWrapper
from ..Model.device import Device
from ..Model.room import Room
from ..Model.room import MonoxideState
from ..Model.room import Place
from ..Model.history import History
from ..Model.tadashiHistory import TadashiHistory
from ...Config.Core.configManager import ConfigManager
from ...utils.helper import is_integer


class Sensor(Enum):
    # sensors
    LIGHT = 'com.fibaro.lightSensor'
    TEMPERATURE = 'com.fibaro.temperatureSensor'
    MOTION = ['com.fibaro.FGMS001v2', 'com.fibaro.motionSensor']
    HUMIDITY = ['com.fibaro.FGFS101', 'com.fibaro.humiditySensor']
    GAZ = 'com.fibaro.FGSS001'
    DOOR = 'com.fibaro.doorSensor'
    SHUTTER = 'com.fibaro.windowSensor'
    NOISE = 'noiseSensor'
    VACCUM = 'vaccumSensor'

    # controllers
    WALL_PLUG = 'FGWP102'
    DIMMER = 'FGWD111'
    SWITCH = 'FGWDS221'
    ROLLER = 'FGWR111'


class FibaroSnapshotManager:
    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))
        self._fibaro_snapshot = History()
        self._tadashi_history = TadashiHistory()
        self._room_logs = {}
        self._response = ''
        self._context = None

    def set_context(self, context):
        self._context = context

    def get_snapshot(self):
        for name, member in Place.__members__.items():
            self._room_logs[name] = Room(member)

        auth_configs = ConfigManager.get_instance().get('fibaro_api')
        api_wrapper = FibaroApiWrapper()
        api_wrapper.connect(auth_configs['ip'], auth_configs['user'], auth_configs['password'])
        self._response = api_wrapper.get('devices')

        if self._context:
            self._tadashi_history.context = self._context
        else:
            self._tadashi_history.context = ConfigManager.get_instance().get('default_context')

    def parse(self):
        devices = json.loads(self._response)
        for device_json_array in devices:
            if device_json_array['roomID'] != 0 and device_json_array['visible'] is not False:
                # because room id 0 is not really a room but control devices like home centers or phones
                # and because some hidden devices are not really devices but plugin or sub-component
                device_object = self.build_fibaro_log(device_json_array)
                self._fibaro_snapshot.add_log(device_object)
                self.complete_tadashi_log(device_object)

        for key, log in self._room_logs.items():
            self._tadashi_history.add_log(log)

    def build_fibaro_log(self, device_info):
        log = Device()
        log.id = device_info["id"]
        log.name = device_info["name"]
        log.roomID = device_info["roomID"]
        log.type = device_info["type"]
        log.baseType = device_info["baseType"]
        log.value = device_info["properties"]["value"]
        log.batteryLevel = device_info["properties"]["batteryLevel"] if "batteryLevel" in device_info["properties"] else 100
        log.dead = device_info["properties"]["dead"]
        log.timestamp = self._fibaro_snapshot.timestamp
        return log

    def complete_tadashi_log(self, device_object):
        log = self._room_logs[Place(device_object.roomID).name]
        self.affect_sensor(log, device_object)

    def affect_sensor(self, log, device_object):
        if device_object.type in Sensor.LIGHT.value:
            if float(device_object.value) > 1:
                log.light = True
            else:
                log.light = False
        elif device_object.type in Sensor.TEMPERATURE.value:
            log.temperature = device_object.value
        elif device_object.type in Sensor.MOTION.value:
            if device_object.value in [True, 'true', '1']:
                log.motion = True
            else:
                log.motion = False
        elif device_object.type in Sensor.HUMIDITY.value:
            if device_object.value in [True, 'true', '1']:
                log.humidity = True
            elif is_integer(device_object.value):
                if int(device_object.value) > 90:
                    log.humidity = True
                else:
                    log.humidity = False
            else:
                log.humidity = False
        elif device_object.type in Sensor.GAZ.value:
            if device_object.value == 0:
                log.gaz = MonoxideState.SAFE
            elif device_object.value == 1:
                log.gaz = MonoxideState.MODERATE
            elif device_object.value == 2:
                log.gaz = MonoxideState.DANGEROUS
        elif device_object.type in Sensor.DOOR.value:
            if device_object.value in [True, 'true', '1']:
                log.door = True
            else:
                log.door = False
        elif device_object.type in Sensor.SHUTTER.value:
            if device_object.value in [True, 'true', '1']:
                log.shutter = True
            else:
                log.shutter = False
        elif device_object.type in Sensor.NOISE.value:
            if device_object.value in [True, 'true', '1']:
                log.noise = True
            else:
                log.noise = False
        elif device_object.type in Sensor.VACCUM.value:
            if device_object.value in [True, 'true', '1']:
                log.vaccum = True
            else:
                log.vaccum = False

    def save_fibaro_snapshot(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/tmp/fibaro_snapshot.json'
        self._fibaro_snapshot.save(path)

    def save_tadashi_history(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/tmp/tadashi_history.json'
        self._tadashi_history.save(path)

    def load_tadashi_history(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/tmp/tadashi_history.json'
        self._tadashi_history.load(path)

    @staticmethod
    def _generate_path(path):
        cwd = os.path.dirname(__file__)
        filename = os.path.join(cwd, path)
        return filename
