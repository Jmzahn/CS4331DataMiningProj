import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt

import lib

MTS = lib.loadMTS()
#only grab this many rows : 307916
MTS = MTS.head(307916)
TRAIN_SPLIT = 77
TRAIN_weeks = 11
VAL_weeks = 3
BATCH_SIZE = 3142
BUFFER_SIZE = 10000



#get date info
dates = MTS['date'].values
dateStart = np.datetime64(dates[0])
dateEnd = np.datetime64(dates[-1])
dateRange = np.arange(dateStart, dateEnd+np.timedelta64(1,'D'), dtype='datetime64[D]')
days = len(dateRange)


#grab feature and target data
featuresNames = ['beds', 'helipads', 'nonProf', 'private', 'governm', 'tests', 'positive', 'negative']
features = MTS[featuresNames].values.reshape((days, BATCH_SIZE, len(featuresNames)))
targetsNames = ['cases']
targets = MTS[targetsNames].values.reshape((days, BATCH_SIZE, len(targetsNames)))

validate_features = features[TRAIN_SPLIT:].reshape(VAL_weeks*7, BATCH_SIZE, len(featuresNames))
validate_targets = targets[TRAIN_SPLIT:].reshape(VAL_weeks*7, BATCH_SIZE, len(targetsNames))
features = features[:TRAIN_SPLIT].reshape(TRAIN_weeks*7, BATCH_SIZE, len(featuresNames))
targets = targets[:TRAIN_SPLIT].reshape(TRAIN_weeks*7, BATCH_SIZE, len(targetsNames))
train_data_multi = tf.data.Dataset.from_tensor_slices((features, targets))
val_data_multi = tf.data.Dataset.from_tensor_slices((validate_features, validate_targets))
train_data_multi = train_data_multi.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()
val_data_multi = val_data_multi.batch(BATCH_SIZE).repeat()


model = keras.models.Sequential()
model.add(keras.layers.CuDNNLSTM(7, return_sequences=True, input_shape = features.shape[-2:], time_major=True))
model.add(keras.layers.CuDNNLSTM(7, return_sequences=True))
model.add(tf.keras.layers.Dense((targets.shape[-1])))
model.summary()
model.compile(optimizer='adam', loss='mean_absolute_error')


multi_step_history = model.fit(train_data_multi, epochs=10, steps_per_epoch=77, validation_data=val_data_multi, validation_steps=21)

