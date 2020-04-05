
import os

import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame
from sklearn.feature_extraction.text import CountVectorizer

from project.load_model import model
from project.model import Tweets, engine
from project.stream.streamer import session
from project.tokenize import tokenize

#Load data from DB (for visualizations)
states = pd.read_csv(os.path.join('data', 'states.csv'))
df = pd.concat([pd.read_csv(os.path.join('data', '21000.csv')), pd.read_csv(os.path.join('data', '4500.csv'))])
final = df.merge(states[['State', 'Code']], left_on='STATE_NAME', right_on='State')
fips = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/laucnty16.csv')

#Create crosstab of Counties vs. Word Counts
class Crosstab:
    '''Class for creating crosstabulation of Counties vs Word Counts from CountVectorizer for input into Choropleth map'''
    def __init__(self, frac=0.1):
        #Subsample full dataframe to conserve memory
        sample = final.sample(axis=0, frac=0.1, random_state=7)
        #Create dense document term matrix
        sparse = model['counter'].fit_transform(sample['tweet']).todense()
        dtm = pd.DataFrame(sparse, columns=model['counter'].get_feature_names())
        #Add respective county to each observation
        dtm_counties = pd.merge(sample, dtm, left_index=True, right_index=True)
        dtm_counties['county'] = dtm_counties['county_name'] + ' County, ' + dtm_counties['Code']
        #Add FIPS identifier for choropleth map
        self.crosstab = dtm_counties.iloc[:,10:].groupby('county').sum()
        self.crosstab = self.crosstab.merge(fips[['State FIPS Code','County FIPS Code','County Name/State Abbreviation']],
                                  how='left', left_on='county', right_on='County Name/State Abbreviation')
        self.crosstab['fips'] = self.crosstab['State FIPS Code'].astype('str').str.zfill(2) + self.crosstab['County FIPS Code'].astype('str').str.zfill(3)
    def get_crosstab(self):
        return self.crosstab
    def filter(self, query):
        return self.crosstab[query.lower()]
#Series of Model Coefficients
