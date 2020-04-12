import os
import yaml
from .Fibaro.Api.fibaroApiWrapper import FibaroApiWrapper
from .Fibaro.Core.fibaroSnapshotManager import FibaroSnapshotManager
from .Map.Core.houseMapper import HouseMapper
from .Fibaro.Core.linker import Linker
from .Monitoring.Core.monitoringManager import MonitoringManager
from .Keras.Core.kerasManager import KerasManager as Keras
from .utils.periodicallyProcessor import PeriodicallyProcessor


class Tadashi:
    DEBUG = False

    _city = None
    _context = None

    def __init__(self, city=None, context=None):
        if city:
            self._city = city
        if context:
            self._context = context

        self._absolute_path = os.path.abspath(os.path.dirname(__file__))

    def process(self, city, context=None):
        self._city = city
        if context:
            self._context = context

        pp = PeriodicallyProcessor()
        callback = self.compute
        pp.process(callback)

    def compute(self, timestamp):
        if self.DEBUG:
            timestamp = 'test'

        self.get_fibaro_snapshot(timestamp)
        self.generate_map(timestamp)
        self.link_map()
        self.predict_and_execute(timestamp)
        self.overwatch(timestamp)

        if self.DEBUG:
            exit()
        else:
            self.delete_tmp_files()

    def get_fibaro_snapshot(self, timestamp):
        print('Gathering Fibaro sensor data...')

        f_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_f.json'
        t_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_t.json'

        fsm = FibaroSnapshotManager()
        fsm.set_context(self._context)
        fsm.get_snapshot()
        fsm.parse()
        fsm.save_fibaro_snapshot(f_path)
        fsm.save_tadashi_history(t_path)

    def generate_map(self, timestamp):
        print('Building home map...')

        t_path = self._absolute_path + '/assets/tmp/' + str(timestamp) + '_t.json'
        svg_path = self._absolute_path + '/assets/map/' + str(timestamp) + '.svg'

        hm = HouseMapper(self._city)
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
        m.trace()

    def link_map(self):
        print('Linking map...')

        tmp_path = self._absolute_path + '/assets/tmp/'
        output_linked_label_path = self._absolute_path + '/assets/model/link.dat'

        linker = Linker()
        linker.link(tmp_path, output_linked_label_path)

    def predict_and_execute(self, timestamp):
        print('Predicting...')
        input_model_path = self._absolute_path + '/assets/model/model.bin'
        input_label_bin_path = self._absolute_path + '/assets/model/mlb.pickle'

        img_to_labalize = self._absolute_path + '/assets/map/' + str(timestamp) + '.svg'

        if not os.path.exists(input_model_path) or not os.path.exists(input_label_bin_path) or not os.path.exists(img_to_labalize):
            return

        keras = Keras()
        labels = keras.classify(input_model_path, input_label_bin_path, img_to_labalize)

        print('Execution')
        for label in labels:
            if label != 'NOTHING_TO_DO':
                device_to_activate = label.split('#')
                print("\t --> device #" + device_to_activate[0] + ": " + device_to_activate[1])
                self.apply_action_on_device(device_to_activate[0], device_to_activate[1])

    def apply_action_on_device(self, device_to_activate, state):
        with open(self._absolute_path + '/config/config.yaml', 'r') as stream:
            try:
                auth_configs = yaml.safe_load(stream)['fibaro_api']
            except yaml.YAMLError as e:
                raise e

        api_wrapper = FibaroApiWrapper()
        api_wrapper.connect(auth_configs['ip'], auth_configs['user'], auth_configs['password'])
        api_wrapper.post(device_to_activate, state)

    def delete_tmp_files(self):
        print('Cleaning!')

        tmp_dir_name = self._absolute_path + '/assets/tmp/'

        linker = Linker()
        two_last_files = linker.get_two_last_files(tmp_dir_name, '*_f.json')

        tmp_files = os.listdir(tmp_dir_name)
        for file in tmp_files:
            if file.endswith(".json") and two_last_files != [] and tmp_dir_name + file not in two_last_files:
                f0 = tmp_dir_name + file
                if os.path.exists(f0):
                    os.remove(f0)
