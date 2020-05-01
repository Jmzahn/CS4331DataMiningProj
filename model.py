import os

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import keras.backend as K


import lib

class Model:
    modelFile = 'model.h5'

    def __init__(self, forceReload=False, save=True, iterations = 100):
        print('Initializing model...')

        if not forceReload and os.path.isfile(self.modelFile):
            self.load()

        else:
            # instantiate and train model
            features, targets, validate_features, validate_targets, dateRange = lib.loadNNData()

            #data_mean = features.mean(axis=0)
            #data_std = features.std(axis=0)
            #for feature in features:
            #    feature = np.divide((feature-data_mean),data_std)

            train_data_multi = tf.data.Dataset.from_tensor_slices((features, targets))
            val_data_multi = tf.data.Dataset.from_tensor_slices((validate_features, validate_targets))
            train_data_multi = train_data_multi.cache().batch(7).shuffle(10000).repeat()#.window(7,drop_remainder=True)
            val_data_multi = val_data_multi.repeat().batch(1)
            print('Instantiating neural network...')
            self.model = keras.models.Sequential()
            self.model.add(tf.compat.v1.keras.layers.CuDNNLSTM(24, return_sequences=True,  input_shape =( features.shape[-2], features.shape[-1]), time_major=True))#
            self.model.add(tf.compat.v1.keras.layers.CuDNNLSTM(12, return_sequences=True))
            self.model.add(tf.keras.layers.Dense(3))
            self.model.add(tf.keras.layers.Dense(targets.shape[-1]))
            self.model.summary()
            print('Compiling neural network...')
            #quantile = 0.5
            #lambda y,f: tilted_loss(quantile,y,f)
            
            self.model.compile(loss='huber_loss', optimizer='adam')#, metrics=['accuracy']
            print('Training Neural network...')
            self.model.fit(train_data_multi, steps_per_epoch=12, epochs=iterations, validation_data=(val_data_multi),validation_steps=7)
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

def tilted_loss(q,y,f):
    e = (y-f)
    return K.mean(K.maximum(q*e, (q-1)*e), axis=-1)