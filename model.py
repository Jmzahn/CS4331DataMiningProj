import os

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras


class Model:
    modelFile = 'model.h5'

    def __init__(self, forceReload=False, save=True):
        print('Initializing model...')

        if not forceReload and os.path.isfile(self.modelFile):
            self.load()

        else:
            # instantiate and train model
            print('Instantiating neural network...')
            #TODO
    
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
