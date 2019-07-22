import os
from Keras.Core.kerasManager import KerasManager as Keras

absolute_path = os.path.abspath(os.path.dirname(__file__))
output_model_path = absolute_path + '/assets/model/model.bin'
output_label_bin_path = absolute_path + '/assets/model/mlb.pickle'

keras = Keras()
keras.train(output_model_path, output_label_bin_path)
