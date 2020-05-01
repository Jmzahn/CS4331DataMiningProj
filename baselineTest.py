import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

import lib

features, targets, validate_features, validate_targets, dateRange = lib.loadNNData()

targets = np.sum(targets, axis=1)
validate_targets = np.sum(validate_targets, axis=1)
index = np.arange(len(targets))
slope, intercept, r_value, p_value, std_err = linregress(index,np.squeeze(targets))

histIndex = np.arange(len(targets))
futureIndex = np.arange(len(targets),len(targets)+len(validate_targets))

predictions=[pred*slope+intercept for pred in futureIndex] 

predIndex = np.arange(len(targets),len(targets)+len(predictions))


plt.figure()
plt.plot(histIndex, targets, 'b--', label='History')
plt.plot(futureIndex, validate_targets, 'b:', label='Future')
plt.plot(predIndex, predictions, 'r:', label='Prediction')
plt.ylabel('Cases as proportion of Pop')
plt.xlabel('Time')
plt.legend(loc='upper left')
plt.show()