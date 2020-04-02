import joblib
import os

import pandas as pd
import geopandas as gpd
from geopandas import GeoDataFrame

from project.model import Tweets, engine
from project.stream.streamer import session
from project.tokenize import tokenize

#Load data from DB (for visualizations)
df = pd.read_csv(os.path.join('data', '21000.csv'))

#Load pickle
model = joblib.load(os.path.join('pickles', 'nb_truncated_tweets'))