#CS4331 Jacob Zahn
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

sys.path.append('..')
import lib

CCH = lib.loadCCHTimeSeries()

beds = CCH['beds'].to_numpy()
population = CCH['population'].to_numpy()
helipads = CCH['helipads'].to_numpy()
nonProf = CCH['nonProf'].to_numpy()
private = CCH['private'].to_numpy()
governm = CCH['governm'].to_numpy()
totalHosp = nonProf + private + governm
casesLast = CCH['c2020-04-12'].to_numpy()
deathsLast = CCH['d2020-04-12'].to_numpy()

bedsZ = stats.zscore(beds)
populationZ = stats.zscore(population)

print('Explore multivariate relationships among the variables')
plt.figure()
plt.scatter(population,beds, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('beds vs population, colored by cases')
plt.xlabel('County population')
plt.ylabel('County hospital beds')

plt.figure()
plt.scatter(populationZ,bedsZ, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('beds vs population, colored by cases')
plt.xlabel('County population Z')
plt.ylabel('County hospital beds Z')



plt.figure()
plt.scatter(population,nonProf, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('Non profit hospitals per person vs cases')
plt.xlabel('Non profit hospitals per person')
plt.ylabel('Cases')

plt.figure()
plt.scatter(population,private, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('Private hospitals per person vs cases')
plt.xlabel('Private hospitals per person')
plt.ylabel('Cases')

plt.figure()
plt.scatter(population,governm, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('Government hospitals per person vs cases')
plt.xlabel('Government hospitals per person')
plt.ylabel('Cases')

plt.show()

print('\nDerive new variables basesd on a combination of existing variables')
plt.figure()
plt.scatter(10000*(beds/population),casesLast)
plt.title('beds per 10000 people vs cases')
plt.xlabel('County beds per 10,000 people')
plt.ylabel('Cases')

plt.figure()
plt.scatter(population,totalHosp, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('Hospitals per person vs cases')
plt.xlabel('Hospitals per person')
plt.ylabel('Cases')

plt.show()