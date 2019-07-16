import os
import datetime
from .Fibaro.Core.fibaroSnapshotManager import FibaroSnapshotManager
from .Map.Core.houseMapper import HouseMapper
from .Fibaro.Core.linker import Linker
from .Monitoring.Core.monitoringManager import MonitoringManager
from .utils.lockManager import LockState
from .utils.lockManager import LockManager
from .utils.periodicallyProcessor import PeriodicallyProcessor


class Tadashi:
    DEBUG = False

    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))
        self._lock_manager = LockManager(60 * 60 * 24 * 3)

    def process(self, city):
        self._city = city
        pp = PeriodicallyProcessor()
        callback = self.compute
        pp.process(callback)

    def compute(self, timestamp):
        if self.DEBUG:
            timestamp = 'test'
            
        self.get_fibaro_snapshot(timestamp)
        self.generate_map(timestamp)
        self.link_map()
        self.predict()
        self.overwatch(timestamp)
        
        # every 3 days, after 3h of the morning, a new model is trained
        if datetime.datetime.now().hour > 3 and self._lock_manager.has_lock('tadashi') == LockState.GOT:
            self.learning(timestamp)
            
        if self.DEBUG:
            exit()
        else:
            self.delete_tmp_files()

    def get_fibaro_snapshot(self, timestamp):
        print('Gathering Fibaro sensor info...')
    
        f_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_f.json'
        t_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_t.json'
        
        fsm = FibaroSnapshotManager()
        fsm.get_snapshot()
        fsm.parse()
        fsm.save_fibaro_snapshot(f_path)
        fsm.save_tadashi_history(t_path)

    def generate_map(self, timestamp):
        print('Building home map...')
        
        t_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_t.json'
        svg_path = self._absolute_path + '/assets/map/' + str(timestamp) + '.svg'
        
        fsm = FibaroSnapshotManager()
        hm = HouseMapper(self._city, fsm)
        hm.load_tadashi_history(t_path)
        hm.parse()
        hm.draw(svg_path)

    def overwatch(self, timestamp):
        print('Monitoring...')
        
        f_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_f.json'
        m_path = self._absolute_path + '/assets/monitoring/monitoring.json'
        
        m = MonitoringManager()
        m.load_fibaro_snapshot(f_path)
        m.load_metrology(m_path)
        m.compute()
        m.save_metrology(m_path)
        m.trace(timestamp)
        
    def link_map(self):
        print('Linking map...')
        
        tmp_path = self._absolute_path + '/assets/tmp/'
        map_path = self._absolute_path + '/assets/map/'
        output_linked_label_path = self._absolute_path + '/assets/model/link.dat'
        
        linker = Linker()
        linker.link(tmp_path, map_path, output_linked_label_path)
        
    def predict(self):
        print('Predicting!')

    def learning(self, timestamp):
        print('Learning!')

    def delete_tmp_files(self):
        print('Cleaning!')
        
        tmp_dir_name = self._absolute_path + '/assets/tmp/'
        monitoring_dir_name = self._absolute_path + '/assets/monitoring/'
        
        linker = Linker()
        two_last_files = linker.get_two_last_files(tmp_dir_name, "*_f.json")
        
        tmp_files = os.listdir(tmp_dir_name)
        for file in tmp_files:
            if file.endswith(".json") and two_last_files != [] and tmp_dir_name + file not in two_last_files:
                f0 = tmp_dir_name + file
                if os.path.exists(f0):
                    os.remove(f0)


