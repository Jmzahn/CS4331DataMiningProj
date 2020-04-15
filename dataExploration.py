import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

import lib

CCH = lib.loadCCHTimeSeries()

beds = CCH['beds'].to_numpy()
population = CCH['population'].to_numpy()
helipads = CCH['helipads'].to_numpy()
nonProf = CCH['nonProf'].to_numpy()
private = CCH['private'].to_numpy()
governm = CCH['governm'].to_numpy()
totalHosp = nonProf + private + governm
casesLast= CCH['c2020-04-12'].to_numpy()

bedsZ = stats.zscore(beds)
populationZ = stats.zscore(population)

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
plt.ylabel('Cases')

plt.figure()
plt.scatter(nonProf,casesLast)
plt.title('Non profit hospitals vs cases')
plt.xlabel('Non profit hospitals')
plt.ylabel('Cases')

plt.figure()
plt.scatter(private,casesLast)
plt.title('Private hospitals vs cases')
plt.xlabel('Private hospitals')
plt.ylabel('Cases')

plt.figure()
plt.scatter(governm,casesLast)
plt.title('Government hospitals vs cases')
plt.xlabel('Government hospitals')
plt.ylabel('Cases')

plt.figure()
plt.scatter(totalHosp,casesLast)
plt.title('Hospitals vs cases')
plt.xlabel('Hospitals')
plt.ylabel('Cases')

plt.figure()
plt.scatter(nonProf/population,casesLast)
plt.title('Non profit hospitals per person vs cases')
plt.xlabel('Non profit hospitals per person')
plt.ylabel('Cases')

plt.figure()
plt.scatter(private/population,casesLast)
plt.title('Private hospitals per person vs cases')
plt.xlabel('Private hospitals per person')
plt.ylabel('Cases')

plt.figure()
plt.scatter(governm/population,casesLast)
plt.title('Government hospitals per person vs cases')
plt.xlabel('Government hospitals per person')
plt.ylabel('Cases')

plt.figure()
plt.scatter(totalHosp/population,casesLast)
plt.title('Hospitals per person vs cases')
plt.xlabel('Hospitals per person')
plt.ylabel('Cases')

plt.figure()
plt.scatter(bedsZ,casesLast)
plt.title('casesLast vs beds')
plt.xlabel('County hospital beds Z')
plt.ylabel('County cases')

plt.figure()
plt.scatter(populationZ,bedsZ, c=casesLast, cmap=matplotlib.cm.cool)
plt.title('beds vs population, colored by cases')
plt.xlabel('County population Z')
plt.ylabel('County hospital beds Z')

plt.show()