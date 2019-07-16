import os
import glob
from ..Model.history import History


class Linker:
    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))

    def link(self, tmp_path=None, map_path=None, output_path=None):
        if not output_path:
            output_path = self._absolute_path + '/../../assets/model/link.dat'
        
        files = self.get_two_last_files(tmp_path, '*_f.json')

        if len(files) >= 2:
            two_last = files[-2:]
            previous_devices = History()
            current_devices = History()
            previous_devices.load(two_last[0])
            current_devices.load(two_last[1])
            
            diff = self.diff(previous_devices.logs, current_devices.logs)
            
            timestamp = os.path.basename(two_last[0]).replace('_f.json', '')
            
            device = 'NOTHING_TO_DO'
            if len(diff) >= 1:
                diff = diff[0]
                device = str(diff.id) + '#' + str(diff.roomID) + '#' + diff.type + '#' + str(diff.value)
            
            with open(output_path, 'a+') as file:
                file.write(device + '\t' + str(timestamp) + '\n')
    
    def diff(self, first, second):
            set1 = set((x.type, x.roomID, x.value) for x in first)
            return [x for x in second if (x.type, x.roomID, x.value) not in set1]
            
    def get_two_last_files(self, tmp_path, filename):
        files = sorted(glob.glob(tmp_path + filename))
        if len(files) >= 2:
            return files[-2:]
        else:
            return []

