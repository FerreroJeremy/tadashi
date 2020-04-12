import os
import json
import yaml
from enum import Enum
from ..Api.fibaroApiWrapper import FibaroApiWrapper
from ..Model.device import Device
from ..Model.room import Room
from ..Model.room import MonoxideState
from ..Model.room import Place
from ..Model.history import History
from ..Model.tadashiHistory import TadashiHistory
from ..Model.tadashiHistory import Context


class Sensor(Enum):
    # sensors
    LIGHT = 'lightSensor'
    TEMPERATURE = 'temperatureSensor'
    MOTION = 'FGMS001v2'
    HUMIDITY = 'FGFS101'
    GAZ = 'motionSensor'
    OPENING = 'doorSensor'
    NOISE = 'noiseSensor'
    VACCUM = 'vaccumSensor'

    # controllers
    WALL_PLUG = 'FGWP102'
    DIMMER = ''
    SWITCH = ''
    CONTROLLER = ''
    ROLLER = ''
    WALLI = ''


class FibaroSnapshotManager:
    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))
        self._fibaro_snapshot = History()
        self._tadashi_history = TadashiHistory()
        self._room_logs = {}
        self._response = ''

    def get_snapshot(self):
        for name, member in Place.__members__.items():
            self._room_logs[name] = Room(member)

        self._tadashi_history.context = Context.UNKNOWN  # feature not implemented yet

        with open(self._absolute_path + '/../../config/config.yaml', 'r') as stream:
            try:
                auth_configs = yaml.safe_load(stream)['fibaro_api']
            except yaml.YAMLError as e:
                raise e

        api_wrapper = FibaroApiWrapper()
        api_wrapper.connect(auth_configs['ip'], auth_configs['user'], auth_configs['password'])
        self._response = api_wrapper.get('devices')

    def parse(self):
        devices = json.loads(self._response)
        for device in devices:
            if device['roomID'] != 0 and device['visible'] is not False and device['baseType'] != 'com.fibaro.device':
                # because room id 0 is not really a room but control devices like home centers or phones
                # and because some hidden devices are not really devices but plugin or sub-component
                fibaro_log = self.build_fibaro_log(device)
                self._fibaro_snapshot.add_log(fibaro_log)
                self.complete_tadashi_log(device)

        for key, log in self._room_logs.items():
            self._tadashi_history.add_log(log)

    def build_fibaro_log(self, device_info):
        if Sensor.LIGHT.value in device_info["type"]:
            if float(device_info["properties"]["value"]) > 5:
                device_info["properties"]["value"] = True
            else:
                device_info["properties"]["value"] = False

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

    def complete_tadashi_log(self, device_info):
        log = self._room_logs[Place(device_info["roomID"]).name]
        self.affect_sensor(log, device_info)

    def affect_sensor(self, log, device_info):
        if Sensor.LIGHT.value in device_info["type"]:
            if float(device_info["properties"]["value"]) > 1:
                log.light = True
            else:
                log.light = False
        elif Sensor.TEMPERATURE.value in device_info["type"]:
            log.temperature = device_info["properties"]["value"]
        elif Sensor.MOTION.value in device_info["type"]:
            if device_info["properties"]["value"] in [True, 'true', '1']:
                log.motion = True
            else:
                log.motion = False
        elif Sensor.HUMIDITY.value in device_info["type"]:
            if device_info["properties"]["value"] in [True, 'true', '1']:
                log.humidity = True
            else:
                log.humidity = False
        elif Sensor.GAZ.value in device_info["type"]:
            if device_info["properties"]["value"] == 0:
                log.gaz = MonoxideState.SAFE
            elif device_info["properties"]["value"] == 1:
                log.gaz = MonoxideState.MODERATE
            elif device_info["properties"]["value"] == 2:
                log.gaz = MonoxideState.DANGEROUS
        elif Sensor.OPENING.value in device_info["type"]:  # find a way to discrimine door and shutter (w/ id maybe?)
            if device_info["properties"]["value"] in [True, 'true', '1']:
                log.door = True
            else:
                log.door = False
        elif Sensor.NOISE.value in device_info["type"]:
            if device_info["properties"]["value"] in [True, 'true', '1']:
                log.noise = True
            else:
                log.noise = False
        elif Sensor.VACCUM.value in device_info["type"]:
            if device_info["properties"]["value"] in [True, 'true', '1']:
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
