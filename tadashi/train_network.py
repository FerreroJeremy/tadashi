import os
import datetime
from .utils.lockManager import LockState
from .utils.lockManager import LockManager
from .utils.periodicallyProcessor import PeriodicallyProcessor
from .Keras.Core.kerasManager import KerasManager as Keras

absolute_path = os.path.abspath(os.path.dirname(__file__))
output_model_path = absolute_path + '/assets/model/model.bin'
output_label_bin_path = absolute_path + '/assets/model/mlb.pickle'

lock_manager = LockManager(60 * 60 * 24 * 3)
keras = Keras()


def compute(timestamp):
    # every 3 days, after 3h of the morning, a new model is trained
    if datetime.datetime.now().hour > 3 and lock_manager.has_lock('training') == LockState.GOT:
        keras.train(output_model_path, output_label_bin_path)


pp = PeriodicallyProcessor()
callback = compute
pp.process(callback)
