"""
This script is designed to process and analyze a collection of academic papers. 
It focuses on papers published after the year 2000, applying text preprocessing and 
language filtering to ensure data quality. The script utilizes the BERTopic model 
to perform topic modeling on the abstracts of these papers. The main steps include:

1. Loading the dataset of academic papers.
2. Filtering papers based on the year of publication and the presence of an abstract.
3. Sampling a subset of 200,000 papers for analysis.
4. Preprocessing the text of these papers and ensuring they are in English.
5. Training a BERTopic model on the processed abstracts.
"""

import json
import random
import fasttext
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from bertopic.vectorizers import ClassTfidfTransformer
from bertopic.representation import KeyBERTInspired

# Import text preprocessing functions 
from preprocessing.research_data_processing import preprocess_abstracts, is_english_fasttext

# Load the dataset of academic papers
cse_data = json.load(open('computer_science_papers_integrated_data.json', 'r'))

# Filter the dataset for papers published after the year 2000 and having an abstract
cse_data_filtered = [data for data in cse_data 
                     if 'year' in data and data['year'] is not None and int(data['year']) > 2000 
                     and data.get('abstract')]

# Sample a subset of 200,000 papers using a specific random seed for reproducibility
random.seed(42)
cse_data_sampled = random.sample(cse_data_filtered, 200000)

# Preprocess abstracts and filter out non-English texts
cse_data_sampled = [data for data in cse_data_sampled if is_english_fasttext(data['abstract'])]
english_abstracts_list = [preprocess_abstracts(data['abstract']) for data in cse_data_sampled]

# Set up the components for the BERTopic model
embedding_model = SentenceTransformer('sentence-transformers/allenai-specter')
umap_model = UMAP(n_neighbors=10, n_components=5, min_dist=0.0, metric='cosine')
hdbscan_model = HDBSCAN(min_cluster_size=10, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
vectorizer_model = CountVectorizer(stop_words="english", min_df=5, ngram_range=(1, 3))
ctfidf_model = ClassTfidfTransformer()
representation_model = KeyBERTInspired()

# Initialize and train the BERTopic model
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    representation_model=representation_model
)
topics, probabilities = topic_model.fit_transform(english_abstracts_list)

# save the trained model for later use
topic_model.save("trained_topic_model")
