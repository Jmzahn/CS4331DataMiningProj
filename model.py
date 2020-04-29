import os

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras

import lib

class Model:
    modelFile = 'model.h5'

    def __init__(self, forceReload=False, save=True):
        print('Initializing model...')

        if not forceReload and os.path.isfile(self.modelFile):
            self.load()

        else:
            # instantiate and train model
            features, targets, validate_features, validate_targets = lib.loadNNData()
            train_data_multi = tf.data.Dataset.from_tensor_slices((features, targets))
            val_data_multi = tf.data.Dataset.from_tensor_slices((validate_features, validate_targets))
            train_data_multi = train_data_multi.cache().shuffle(10000).batch(3142).repeat()
            val_data_multi = val_data_multi.batch(3142).repeat()
            print('Instantiating neural network...')
            self.model = keras.models.Sequential()
            self.model.add(keras.layers.CuDNNLSTM(7, return_sequences=True, input_shape = features.shape[-2:], time_major=True))
            self.model.add(keras.layers.CuDNNLSTM(7, return_sequences=True))
            self.model.add(tf.keras.layers.Dense((targets.shape[-1])))
            self.model.summary()
            print('Compiling neural network...')
            self.model.compile(optimizer='adam', loss='mean_absolute_error')
            print('Training Neural network...')
            self.model.fit(train_data_multi, epochs=10, steps_per_epoch=77, validation_data=val_data_multi, validation_steps=21)
            if save:
                self.save()
    
    # load model from file
    def load(self):
        print('Loading model from file...')
        self.model = keras.models.load_model(self.modelFile)
    
    # save model to file
    def save(self):
        print('Saving model...')
        self.model.save(self.modelFile)

    def predict(self, embeddings):
        print('Making predictions on neural network...')
        modelPredictions = self.model.predict(embeddings)
        print('Done making predictions.')
        return modelPredictions

    # retrain model
    def retrain(self, train_embeddings, train_labels, iterations=5, save=True):
        print('Training neural network...')
        self.model.fit(train_embeddings, train_labels, epochs=iterations)
        if save:
            self.save()

    # tests for accuracy
    def test(self, test_data, test_labels):
        print('Testing model...')
        test_loss, test_acc = self.model.evaluate(test_data, test_labels)
        print('Neural network accuracy: {}%'.format(test_acc * 100))
