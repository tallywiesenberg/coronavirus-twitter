import en_core_web_sm
import spacy

nlp = en_core_web_sm.load()

def tokenize(doc):
    return [token.text for token in nlp(doc) 
            if (token.pos_ not in set(['PUNCT', 'ADP', 'NUM', 'SPACE', 'PRON', 'DET', 'AUX', 'PART']))
            and (token.text not in set(['#', 'coronavirus', 'covid', '𝚌𝚘𝚛𝚘𝚗𝚊𝚟𝚒𝚛𝚞𝚜', '@']))
            and token.like_url == False
            and token.is_stop == False]