
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
df = pd.concat([pd.read_csv(os.path.join('data', '21000.csv')), pd.read_csv(os.path.join('data', '4500.csv'))])


#Create crosstab of Counties vs. Word Counts
class Crosstab:
    def __init__(self, frac=0.1):
        sample = df.sample(axis=0, frac=0.1, random_state=7)
        sparse = model['counter'].fit_transform(sample['tweet']).todense()
        dtm = pd.DataFrame(sparse, columns=model['counter'].get_feature_names())
        dtm_counties = pd.merge(sample, dtm, left_index=True, right_index=True)
        dtm_counties['county'] = dtm_counties['county_name'] + ', ' + dtm_counties['STATE_NAME']
        self.crosstab = dtm_counties.iloc[:,10:].groupby('county').sum()
    def get_crosstab(self):
        return self.crosstab
    def filter(self, query):
        return self.crosstab[query]
#Series of Model Coefficients
