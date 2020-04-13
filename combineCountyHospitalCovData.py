import time

import numpy as np
import pandas as pd

import lib

#load new dataset 
CountyHospital = lib.loadCHCombined()
#load NYTimes data
CountyCovData = lib.loadUSCountiesCov()

#grab dates and turn them into numpy variable
DAYBEFORE = '2020-01-20'
DAYBEFORE = np.datetime64(DAYBEFORE)
dates = CountyCovData['date']
dates = np.array(dates, dtype=np.datetime64)

#make a range of dates so we know current dataset length in days
dateRange = np.arange(DAYBEFORE, dates[-1], dtype=np.datetime64)

#make lists that are shape (days*county, )
casesPerCountyPerDay = np.zeros((len(dateRange)*len(CountyHospital)),dtype=np.intc)
deathsPerCountyPerDay = np.zeros((len(dateRange)*len(CountyHospital)),dtype=np.intc)

#POPEST2019,BEDS,HELIPADS,NONPROF,PRIVATE,GOVERNM,LAT,LON
#grab county state from hospital and cov data
counties = CountyHospital['COUNTY'].to_numpy()
states = CountyHospital['STATE'].to_numpy()
populations = CountyHospital['POPEST2019'].to_numpy()
beds = CountyHospital['BEDS'].to_numpy()
helipads = CountyHospital['HELIPADS'].to_numpy()
nonProf = CountyHospital['NONPROF'].to_numpy()
private = CountyHospital['PRIVATE'].to_numpy()
governm = CountyHospital['GOVERNM'].to_numpy()
lat = CountyHospital['LAT'].to_numpy()
lon = CountyHospital['LON'].to_numpy()

countiesHolder=np.array(counties, dtype=str)

for n, county in enumerate(counties):
    if(county.endswith(' County')):
        county = county[:-7]
    if(county.endswith(' Borough')):
        county = county[:-8]
    if(county.endswith(' Municipality')):
        county = county[:-13]
    if(county.endswith(' Census Area')):
        county = county[:-12]
    if(county.endswith(' Parish')):
        county = county[:-7]
    countiesHolder[n] = county


covCounties = CountyCovData['county'].to_numpy()
covStates = CountyCovData['state'].to_numpy()
covCases = CountyCovData['cases'].to_numpy()
covDeaths = CountyCovData['deaths'].to_numpy()

start = time.time()
#now we have to make an O(3142^2+n^2) nested loop to fill the cases and deaths lists
d = np.intc(0)
while(d<len(dateRange)):
    date=dateRange[d]
    c = np.intc(0)
    while(c<len(countiesHolder)):
        county = countiesHolder[c]
        state = states[c]
        stateAndCountyMap = (covCounties==county)&(covStates==state)
        cases = covCases[stateAndCountyMap]
        deaths = covDeaths[stateAndCountyMap]
        datesMap = dates[stateAndCountyMap]==date
        cases = np.sum(cases[datesMap])
        deaths = np.sum(deaths[datesMap])
        casesPerCountyPerDay[d*3142+c] += cases
        deathsPerCountyPerDay[d*3142+c] += deaths
        c += np.intc(1)
    d += np.intc(1)
end = time.time()
ellapsed = end-start
print('big loop took : ',ellapsed,' seconds')

#for d, date in enumerate(dateRange):
#    for c, (county, state) in enumerate(zip(countiesHolder, states)):
#        stateAndCountyMap = (covCounties==county)&(covStates==state)
#        cases = covCases[stateAndCountyMap]
#        deaths = covDeaths[stateAndCountyMap]
#        datesMap = dates[stateAndCountyMap]==date
#        cases = np.sum(cases[datesMap])
#        deaths = np.sum(deaths[datesMap])
#        casesPerCountyPerDay[d+c] += cases
#        deathsPerCountyPerDay[d+c] += deaths




allDatesAllCounties = np.empty((len(dateRange)*len(CountyHospital)),dtype='datetime64[D]')

start = time.time()
for d, date in enumerate(dateRange):
    for c in range(len(CountyHospital)):
        allDatesAllCounties[c+d*3142] = date
end = time.time()
ellapsed = end-start
print('date init loop took : ',ellapsed,' seconds')

allCountiesAllDays      = np.tile(counties, len(dateRange))
allStatesAllDays        = np.tile(states, len(dateRange))
allPopulationsAllDays   = np.tile(populations, len(dateRange))
allBedsAllDays          = np.tile(beds, len(dateRange))
allHelipadsAllDays      = np.tile(helipads, len(dateRange))
allNonProfAllDays       = np.tile(nonProf, len(dateRange))
allPrivateAllDays       = np.tile(private, len(dateRange))
allGovernmAllDays       = np.tile(governm, len(dateRange))
allLatAllDays           = np.tile(lat, len(dateRange))
allLonAllDays           = np.tile(lon, len(dateRange))

dataDict = {
        'date'    : allDatesAllCounties   ,
        'county'    : allCountiesAllDays    ,
        'state'    : allStatesAllDays      ,
        'population'    : allPopulationsAllDays ,
        'beds'    : allBedsAllDays        ,
        'helipads'    : allHelipadsAllDays    ,
        'nonProf'    : allNonProfAllDays     ,
        'private'    : allPrivateAllDays     ,
        'governm'    : allGovernmAllDays     ,
        'lat'    : allLatAllDays         ,
        'lon'    : allLonAllDays         ,
        'cases'    : casesPerCountyPerDay  ,
        'deaths'    : deathsPerCountyPerDay 
}
dataName = './data/CovByCountyHospitalByDates.csv'

lib.saveDictAsCSV(dataDict,dataName)