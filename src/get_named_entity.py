import spacy
from src.exception import CustomException
from src.logger import logging
import sys
try:
    nlp = spacy.load('en_core_web_sm')
except Exception as e:
    raise CustomException(e, sys)

def get_nouns(text):
    doc = nlp(text)
    nouns = [token.text for token in doc if token.pos_ in ['PROPN']]
    return nouns

def compare(required_nouns, found_nouns):
    for noun in required_nouns:
        if noun not in found_nouns:
            return False
    return True

def get_important_texts(other_news, news):
    required_nouns = get_nouns(news)
    imp_texts = []
    for text in other_news:
        found_nouns = get_nouns(text)
        if compare(required_nouns, found_nouns) == True:
            imp_texts.append(text)

    return imp_texts
