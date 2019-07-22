from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K


class ConvolutionalNetwork:
    @staticmethod
    def build(width, height, depth, classe_number, final_activation="softmax"):
        model = Sequential()
        input_shape = (height, width, depth)
        chan_dim = -1

        # if we are using "channels first", update the input shape and channel dimension
        if K.image_data_format() == "channels_first":
            input_shape = (depth, height, width)
            chan_dim = 1

        # CONV => RELU => POOL
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))  # Rectified Linear Unit
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(3, 3)))
        model.add(Dropout(0.25))  # randomly disconnect nodes with the next layer => reduce overfitting

        # (CONV => RELU) * 2 => POOL
        # progressively reduce the spatial size but increase depth
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(64, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # (CONV => RELU) * 2 => POOL
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(Conv2D(128, (3, 3), padding="same"))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chan_dim))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Dropout(0.25))

        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(1024))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        model.add(Dense(classe_number))
        # use softmax activation for single-label classification and sigmoid activation for multi-label classification
        model.add(Activation(final_activation))

        return model
