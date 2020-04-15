import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import lib

CCH = lib.loadCCHTimeSeries()

beds = CCH['beds'].to_numpy()
population = CCH['population'].to_numpy()
casesLast= CCH['c2020-04-12'].to_numpy()

plt.figure()
plt.scatter(population,casesLast)
plt.title('casesLast vs population')
plt.xlabel('County population')
plt.ylabel('County cases')

plt.figure()
plt.scatter(beds,casesLast)
plt.title('casesLast vs beds')
plt.xlabel('County hospital beds')
plt.ylabel('County cases')

plt.figure()
plt.scatter(population,beds, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('beds vs population, colored by cases')
plt.xlabel('County population')
plt.ylabel('County hospital beds')

#clean up scatter to remove non zero elements
nonZeroMap = casesLast!=0

plt.figure()
plt.scatter(population[nonZeroMap],beds[nonZeroMap], c=casesLast[nonZeroMap], cmap=matplotlib.cm.cool)
plt.title('beds vs population, colored by cases\nNo zero cases')
plt.xlabel('County population')
plt.ylabel('County hospital beds')

plt.figure()
plt.scatter(10000*(beds/population),casesLast)
plt.title('beds per 10000 people vs cases')
plt.xlabel('County beds per 10,000 people')
plt.ylabel('County cases')


plt.show()