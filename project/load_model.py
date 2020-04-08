import os
import joblib

import en_core_web_sm
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

nlp = en_core_web_sm.load()

def tokenize(doc):
    return [token.text for token in nlp(doc) 
            if (token.pos_ not in set(['PUNCT', 'ADP', 'NUM', 'SPACE', 'PRON', 'DET', 'AUX', 'PART']))
            and all(x not in token.text for x in ['#', '@', '_', 'corona', 'covid', '&', 'amp', '/', ' '])
            and token.like_url == False
            and token.is_stop == False]

#Load pickle
def load_model():
    return joblib.load(os.path.join('pickles', 'log_25000'))
