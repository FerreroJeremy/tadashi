import os
import glob
from ..Model.history import History
from .fibaroSnapshotManager import Sensor


class Linker:
    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))

    def link(self, tmp_path=None, output_path=None):
        if not output_path:
            output_path = self._absolute_path + '/../../assets/model/link.dat'

        files = self.get_two_last_files(tmp_path, '*_f.json')

        if len(files) >= 2:
            two_last = files[-2:]
            previous_devices = History()
            current_devices = History()
            previous_devices.load(two_last[0])
            current_devices.load(two_last[1])

            differences = self.diff(previous_devices.logs, current_devices.logs)

            map_timestamp = os.path.basename(two_last[0]).replace('_f.json', '')

            device_to_activate = 'NOTHING_TO_DO'

            if len(differences) > 0:
                for diff in differences:
                    # improve later to filter the devices that can be activated by the prediction or not
                    if Sensor.WALL_PLUG.value in diff.type \
                            and Sensor.WALL_PLUG.value in diff.type\
                            and Sensor.DIMMER.value in diff.type\
                            and Sensor.SWITCH.value in diff.type\
                            and Sensor.CONTROLLER.value in diff.type\
                            and Sensor.ROLLER.value in diff.type\
                            and Sensor.WALLI.value in diff.type:
                        device_to_activate = str(diff.id) + '#' + str(diff.value)
                        break

            with open(output_path, 'a+') as file:
                file.write(device_to_activate + '\t' + str(map_timestamp) + '\n')

    def diff(self, first, second):
        _set = set((x.type, x.roomID, x.value) for x in first)
        return [x for x in second if (x.type, x.roomID, x.value) not in _set]

    def get_two_last_files(self, tmp_path, filename):
        files = sorted(glob.glob(tmp_path + filename))
        if len(files) >= 2:
            return files[-2:]
        else:
            return []
