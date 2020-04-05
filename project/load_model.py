import os
import joblib

from project.tokenize import tokenize

#Load pickle
model = joblib.load(os.path.join('pickles', 'nb_25000'))
