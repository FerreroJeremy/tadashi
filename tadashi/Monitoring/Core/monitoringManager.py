import os
import json
import numpy as np
import pandas as pd
from random import *
import matplotlib.pyplot as plt
from ...utils.graphic import Graphic
from ..Model.counter import Counter
from ..Model.monitoring import Monitoring
from ...Fibaro.Model.device import Device
from ...Fibaro.Model.history import History
from ...Fibaro.Core.fibaroSnapshotManager import Sensor


class MonitoringManager:
    def __init__(self):
        self._confusion_matrix = {}
        self._device_info = History()
        self._monitoring = Monitoring()
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))

    def load_fibaro_snapshot(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/tmp/fibaro_snapshot.json'
        self._device_info.load(path)

    def load_metrology(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/monitoring/monitoring.json'
        self._monitoring.load(path)

    def save_metrology(self, path=None):
        if not path:
            path = self._absolute_path + '/../../assets/monitoring/monitoring.json'
        self._monitoring.save(path)

    def compute(self):
        self._confusion_matrix = {}
        previously_timestamp = 0
        for device in self._device_info.logs:
            if Sensor.TEMPERATURE.value not in device.type:
                if Sensor.LIGHT.value in device.type:
                    if float(device.value) > 1:
                        device.value = True
                    else:
                        device.value = False
                is_already_exist = False
                device_name = device.type.replace('com.fibaro.', '') + '#room' + str(device.roomID)
                
                if int(device.batteryLevel) <= 15:
                    self._monitoring.add_alert(device_name + ' battery is low')
                
                if device.dead == True:
                    self._monitoring.add_alert(device_name + ' is dead')
                
                for counter in self._monitoring.metrology:
                    if device.type == counter.type and device.value == counter.value and device.roomID == counter.roomID:
                        counter.count += 1
                        is_already_exist = True
                
                if device.timestamp - previously_timestamp <= 20:
                    counter.corrected += 1
                    device_name = device.type.replace('com.fibaro.', '') + '#room' + str(device.roomID) + '#' + str(device.value)
                    counter_name = counter.type.replace('com.fibaro.', '') + '#room' + str(counter.roomID) + '#' + str(counter.value)
                    if (device_name, counter_name) in self._confusion_matrix:
                        self._confusion_matrix[(device_name, counter_name)] += 1
                    else:
                        self._confusion_matrix[(device_name, counter_name)] = 1
                
                if is_already_exist is False:
                    c = Counter(device.id, device.roomID, device.type, device.baseType, device.value, 1, 0)
                    self._monitoring.add_counter(c)
                previously_timestamp = device.timestamp
        
    def trace(self, timestamp):
        sensor = []
        count = []
        corrected = []
        for counter in self._monitoring.metrology:
            sensor.append(counter.type.replace('com.fibaro.', '') + '#room' + str(counter.roomID) + '#' + str(counter.value))
            count.append(counter.count)
            corrected.append(counter.corrected)
        self.trace_count_curve(timestamp, sensor, count, corrected)
        self.trace_confusion_matrice(timestamp, sensor)

    def trace_count_curve(self, timestamp, sensor, count, corrected):
        # Create a dataframe
        df = pd.DataFrame({'group':sensor, 'value1':count, 'value2':corrected})
        # Reorder it following the values:
        ordered_df = df.sort_values(by='value1')
        my_range=range(1,len(df.index)+1)
        plt.hlines(y=my_range, xmin=ordered_df['value1'], xmax=ordered_df['value2'], color='grey', alpha=0.4)
        plt.scatter(ordered_df['value1'], my_range, color='skyblue', alpha=1, label='count')
        plt.scatter(ordered_df['value2'], my_range, color='red', alpha=0.4 , label='corrected')
        plt.legend()
        # Add title and exis names
        plt.yticks(my_range, ordered_df['group'])
        plt.title("Interactions and corrections of sensors", loc='left')
        plt.xlabel('Value')
        plt.ylabel('Sensor')
        plt.tight_layout()
        plt.savefig(self._absolute_path + '/../../assets/monitoring/metrology.png')
        plt.close()
        
    def trace_confusion_matrice(self, timestamp, sensors):
        list = []
        for sensor1 in sensors:
            row = []
            for sensor2 in sensors:
                if (sensor1, sensor2) in self._confusion_matrix:
                    row.append(self._confusion_matrix[(sensor1, sensor2)])
                else:
                    row.append(0)
            list.append(row)
        
        data = np.array(list)
        
        fig, ax = plt.subplots()
        graph = Graphic()
        im, cbar = graph.heatmap(data, sensors, sensors, ax=ax, cmap="YlGn", cbarlabel="Correlation")
        #texts = graph.annotate_heatmap(im)
        fig.tight_layout()
        plt.savefig(self._absolute_path + '/../../assets/monitoring/confusion_matrice.png')
        plt.close()
        
        


