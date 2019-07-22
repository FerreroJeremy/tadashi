from .convolutionalNetwork import ConvolutionalNetwork
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import matplotlib
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import pickle
import cv2
import os
import cairosvg
import random
import tensorflow as tf
import datetime
import sys


class KerasManager:

    EPOCHS = 75
    INIT_LR = 1e-3
    BS = 32
    IMAGE_DIMS = (96, 96, 3)

    def __init__(self):
        self._absolute_path = os.path.abspath(os.path.dirname(__file__))
        self._input_dataset_path = self._absolute_path + '/../../assets/map'
        self._input_linked_label_path = self._absolute_path + '/../../assets/model/link.dat'
        self._output_graph_path = self._absolute_path + '/../../assets/monitoring/training.png'

    def train(self, output_model_path, output_label_bin_path, input_dataset_path=None, input_linked_label_path=None):
        if input_dataset_path is not None:
            self._input_dataset_path = input_dataset_path

        if input_linked_label_path is not None:
            self._input_linked_label_path = input_linked_label_path

        # For remove Tensorflow warnings and deprecated messages
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

        matplotlib.use("Agg")

        print("Loading images...")

        # Get label-image mapping from the previously builded Linker file
        labels_to_img = []
        with open(self._input_linked_label_path) as f:
            lines = f.read().split('\n')
            for line in lines:
                if line != '':
                    labels_to_img.append(line.split('\t'))

        data = []
        labels = []

        random.seed(42)
        random.shuffle(labels_to_img)

        # Format images
        for label_to_img in labels_to_img:
            label = label_to_img[0]
            svg_img_path = self._input_dataset_path + '/' + label_to_img[1] + '.svg'
            png_img_path = self._input_dataset_path + '/' + label_to_img[1] + '.png'

            cairosvg.svg2png(url=svg_img_path, write_to=png_img_path)

            image = cv2.imread(png_img_path)
            image = cv2.resize(image, (self.IMAGE_DIMS[1], self.IMAGE_DIMS[0]))
            image = img_to_array(image)

            data.append(image)
            labels.append([label])

            if os.path.exists(png_img_path):
                os.remove(png_img_path)

        # scale the raw pixel intensities to the range [0, 1]
        data = np.array(data, dtype="float") / 255.0
        labels = np.array(labels)

        # binarize the labels using scikit-learn special multi-label binarizer implementation
        mlb = MultiLabelBinarizer()
        labels = mlb.fit_transform(labels)

        # print(labels)
        # for (i, label) in enumerate(mlb.classes_):
        #     print("{}. {}".format(i + 1, label))

        print("\t --> {} images ({:.2f}MB) loaded for {} different label(s)".format(len(labels), data.nbytes / (1024 * 1000.0), len(mlb.classes_)))

        # cross validation with 80% of data for training and the remaining 20% for testing
        (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2, random_state=42)

        print("Building model...")

        # initialize the model with a sigmoid final layer in the network to perform multi-label classification
        model = ConvolutionalNetwork.build(width=self.IMAGE_DIMS[1], height=self.IMAGE_DIMS[0], depth=self.IMAGE_DIMS[2], classe_number=len(mlb.classes_), final_activation="sigmoid")

        # initialize the optimizer (SGD is sufficient)
        opt = Adam(lr=self.INIT_LR, decay=self.INIT_LR / self.EPOCHS)

        # compile the model using binary cross-entropy rather than categorical cross-entropy
        model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])

        print("Training network...")

        start = datetime.datetime.now().replace(microsecond=0)

        # construct the image generator for data augmentation
        aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2, horizontal_flip=True, fill_mode="nearest")
        h = model.fit_generator(aug.flow(trainX, trainY, batch_size=self.BS), validation_data=(testX, testY), steps_per_epoch=len(trainX) // self.BS, epochs=self.EPOCHS, verbose=0)

        end = datetime.datetime.now().replace(microsecond=0)

        print("\t --> model builded in " + str(end - start))

        print("Saving model...")

        model.save(output_model_path)
        statinfo = os.stat(output_model_path)
        print("\t --> model of {:.2f}MB saved".format(statinfo.st_size / (1024 * 1000.0)))

        print("Serializing label binarizer...")

        f = open(output_label_bin_path, "wb")
        f.write(pickle.dumps(mlb))
        f.close()

        print("Ploting training loss and accuracy...")

        plt.style.use("ggplot")
        plt.figure()
        n = self.EPOCHS
        plt.plot(np.arange(0, n), h.history["loss"], label="train_loss")
        plt.plot(np.arange(0, n), h.history["val_loss"], label="val_loss")
        plt.plot(np.arange(0, n), h.history["acc"], label="train_acc")
        plt.plot(np.arange(0, n), h.history["val_acc"], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="upper left")
        plt.savefig(self._output_graph_path)

    def classify(self, trained_model_path, label_binarizer_path, input_image_path):
        # For remove Tensorflow warnings and deprecated messages
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

        print("Pre-treating image...")

        png_img_path = input_image_path + '.png'
        cairosvg.svg2png(url=input_image_path, write_to=png_img_path)

        image = cv2.imread(png_img_path)
        image = cv2.resize(image, (96, 96))
        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        if os.path.exists(png_img_path):
            os.remove(png_img_path)

        print("Loading network...")

        model = load_model(trained_model_path)
        mlb = pickle.loads(open(label_binarizer_path, "rb").read())

        print("Classifying image...")

        proba = model.predict(image)[0]
        idxs = np.argsort(proba)[::-1][:2]  # for future feature (multi label classification), we keep two labels

        for (i, j) in enumerate(idxs):
            # just print and return the first, the most likely class/label
            print("\t --> {}: {:.2f}%".format(mlb.classes_[j], proba[j] * 100))
            return mlb.classes_[j]
