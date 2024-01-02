#!/usr/bin/env python
# coding: utf-8

"""
This script contains functions for preprocessing text data, focusing on cleaning, normalization,
and language filtering. These functions are designed to clean and prepare text data for natural 
language processing tasks, particularly for English language texts.
"""

import re
import nltk
import fasttext
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

def preprocess_abstracts(abstract):
    """
    Preprocess the abstracts by removing HTML tags, URLs, non-alphabetic characters, and extra spaces.
    The text is also converted to lowercase.
    """
    abstract = re.sub(r'<.*?>', ' ', abstract)  # Remove HTML tags
    abstract = re.sub(r'http\S+|www\S+|https\S+', ' ', abstract, flags=re.MULTILINE)  # Remove URLs
    abstract = re.sub(r'[^a-zA-Z\s]', ' ', abstract)  # Keep only alphabetic characters
    abstract = abstract.lower()  # Convert to lowercase
    abstract = re.sub('\s+', ' ', abstract)  # Remove extra spaces
    return abstract

def is_english_fasttext(text):
    """
    Check if the given text is in English using the FastText model.
    """
    model = fasttext.load_model('lid.176.ftz')
    predictions = model.predict(text, k=1)
    return predictions[0][0] == '__label__en'

def download_nltk_resources():
    """
    Download necessary NLTK resources for tokenization and stopwords.
    """
    nltk.download('punkt')
    nltk.download('stopwords')

# Running necessary setup
download_nltk_resources()
print("Text preprocessing setup complete.")
