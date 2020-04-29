#library of helper functions
import os
import time

import numpy as np
import pandas as pd



#data from https://hifld-geoplatform.opendata.arcgis.com/datasets/hospitals
def loadHospitals():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/Hospitals.csv')
    return df

#data from https://github.com/nytimes/covid-19-data
def loadUSCountiesCov():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/us-counties.csv')
    return df

#data sheet https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2010-2019/co-est2019-alldata.pdf
#data from https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/
def loadCountyPopEst():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/co-est2019-alldata.csv', encoding='latin-1')
    return df

def loadCHCombined():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/CountyHospitalCombined.csv')
    return df

def loadCCHTimeSeries():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/CovCountyHospitalTimeSeries.csv')
    return df

def loadDailyStateTesting():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/daily.csv')
    return df

def loadSTTS():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/StateTestingTimeSeries.csv')
    return df

def loadMTS():
    df = pd.read_csv(os.path.dirname(__file__)+'/data/MasterTimeSeries.csv.gz')
    return df

def loadNNData():
    MTS = loadMTS()
    #only grab this many rows : 307916
    MTS = MTS.head(307916)
    TRAIN_SPLIT = 77
    TRAIN_weeks = 11
    VAL_weeks = 3
    BATCH_SIZE = 3142
    
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
    return features, targets, validate_features, validate_targets

class Location:#simple class for holding the important location data obtained from Nominatim
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
    def set_name(self, new_name):
        self.name = new_name
    def set_lat(self, new_lat):
        self.lat = new_lat
    def set_lon(self, new_lon):
        self.lon = new_lon

def countyState_to_LatLong(counties, states):
    from geopy.geocoders import Nominatim
    geolocator = Nominatim(user_agent="schoolResearchCounties")
    locObjList = np.empty(counties.shape, dtype=Location)

    for n, (county, state) in enumerate(zip(counties, states)):
        location = county+', '+state
        geoLoc = geolocator.geocode(location, timeout=100)
        if geoLoc is not None:
            loc = Location(name = location,lat = geoLoc.latitude,lon = geoLoc.longitude)
            locObjList[n] = loc
        if(n%100==0):
            print(location+', ', n)
            #print(loc)
            time.sleep(120)
    
    return locObjList

def saveDictAsCSV(data_dict, data_name):
    #create dataframe from dictionary
    df=pd.DataFrame(data_dict)
    #save dataframe as csv
    df.to_csv(data_name,index=False)

stateDict = {
        "AL": "Alabama" 	                                 ,
        "AK": "Alaska" 	                                 ,
        "AZ": "Arizona" 	                                 ,
        "AR": "Arkansas" 	                                 ,
        "CA": "California"                                 ,
        "CO": "Colorado" 	                                 ,
        "CT": "Connecticut"                                ,
        "DE": "Delaware" 	                                 ,
        "DC": "District of Columbia"                       ,
        "FL": "Florida" 	                                 ,
        "GA": "Georgia" 	                                 ,
        "HI": "Hawaii" 	                                 ,
        "ID": "Idaho" 	                                 ,
        "IL": "Illinois" 	 	                             ,
        "IN": "Indiana" 	 	                             ,
        "IA": "Iowa" 	                                     ,
        "KS": "Kansas" 	                                 ,
        "KY": "Kentucky" 	                                 ,
        "LA": "Louisiana" 	                             ,
        "ME": "Maine" 	                                 ,
        "MD": "Maryland"                                   ,
        "MA": "Massachusetts"                              ,
        "MI": "Michigan" 	                                 ,
        "MN": "Minnesota" 	                             ,
        "MS": "Mississippi"                                ,
        "MO": "Missouri" 	                                 ,
        "MT": "Montana" 	                                 ,
        "NE": "Nebraska" 	                                 ,
        "NV": "Nevada" 	                                 ,
        "NH": "New Hampshire"                              ,
        "NJ": "New Jersey"                                 ,
        "NM": "New Mexico"                                 ,
        "NY": "New York" 	                                 ,
        "NC": "North Carolina"                             ,
        "ND": "North Dakota"                               ,
        "OH": "Ohio"                                       ,
        "OK": "Oklahoma" 	                                 ,
        "OR": "Oregon" 	                                 ,
        "PA": "Pennsylvania"                               ,
        "RI": "Rhode Island"                               ,
        "SC": "South Carolina"                             ,
        "SD": "South Dakota" 	                             ,
        "TN": "Tennessee" 	                             ,
        "TX": "Texas" 	                                 ,
        "UT": "Utah" 	                                     ,
        "VT": "Vermont" 	                                 ,
        "VA": "Virginia" 	                                 ,
        "WA": "Washington" 	                             ,
        "WV": "West Virginia" 	                         ,
        "WI": "Wisconsin" 	                             ,
        "WY": "Wyoming" 	                                 ,
        "AS": "American Samoa"                             ,
        "GU": "Guam" 	                                     ,
        "MP": "Northern Mariana Islands" 	                 ,
        "PR": "Puerto Rico" 	                             ,
        "VI": "U.S. Virgin Islands" 	                     ,
        "UM": "U.S. Minor Outlying Islands" 	             ,
        "FM": "Micronesia" 	                             ,
        "MH": "Marshall Islands" 	                         ,
        "PW": "Palau" 	                                 ,
        "AA": "U.S. Armed Forces – Americas[d]"	            ,
        "AE": "U.S. Armed Forces – Europe[e]"	                ,
        "AP": "U.S. Armed Forces – Pacific[f]"	            ,
        "CM": "Northern Mariana Islands Obsolete postal code",
        "PZ": "Panama Canal Zone Obsolete postal code" 	 ,
        "NB": "Nebraska Obsolete postal code"				    ,
        "PH": "Philippine Islands Obsolete postal code" ,  
 	    "PC": "Trust Territory of the Pacific Islands Obsolete postal code"
}
