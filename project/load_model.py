import os
import joblib

#Load pickle
model = joblib.load(os.path.join('pickles', 'nb_25000'))
