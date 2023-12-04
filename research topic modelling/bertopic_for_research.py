import requests  # For making HTTP requests
import json  # For JSON manipulation
import os  # For interacting with the operating system
import gzip  # For working with gzip compressed files
import shutil  # For file operations
import pandas as pd  # For data manipulation and analysis
import re  # For regular expression operations
import numpy as np  # For numerical operations
import multiprocessing as mp  # For parallel processing
import time  # For time-related functions
from langdetect import detect  # For language detection
from sentence_transformers import SentenceTransformer  # For sentence embeddings
from sklearn.feature_extraction.text import TfidfTransformer  # For TF-IDF transformation
from bertopic.representation import KeyBERTInspired  # BERTopic representation
from bertopic.vectorizers import ClassTfidfTransformer  # Class-based TF-IDF vectorizer
from umap import UMAP  # For dimensionality reduction using UMAP
from hdbscan import HDBSCAN  # For clustering
from sklearn.feature_extraction.text import CountVectorizer  # For converting text to a matrix of token counts

# Configure the BERTopic models for topic modeling
embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')
hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
vectorizer_model = CountVectorizer(stop_words="english")
ctfidf_model = ClassTfidfTransformer()
representation_model = KeyBERTInspired()

# Initialize the BERTopic model with the configured models
topic_model = BERTopic(
    embedding_model=embedding_model,          
    umap_model=umap_model,                    
    hdbscan_model=hdbscan_model,              
    vectorizer_model=vectorizer_model,        
    ctfidf_model=ctfidf_model,                
    representation_model=representation_model
)

# Load paper abstracts from a compressed file
paper_abstracts = []
with gzip.open('abstracts_0.gz', 'rt', encoding='utf-8') as f:
    for line in f:
        paper_abstracts.append(json.loads(line.strip()))

# Limit the number of abstracts for processing
paper_abstracts = paper_abstracts[:30000]

# Extract English abstracts and their corresponding corpus IDs
english_abstracts_list = [abst_list['abstract'] for abst_list in paper_abstracts]
english_corpus_ids = [abst_list['corpusid'] for abst_list in paper_abstracts]

# Create a DataFrame with corpus IDs and abstracts
df_abstracts = pd.DataFrame({
    'corpusid': english_corpus_ids,
    'abstract': english_abstracts_list
})

# Disable tokenizer parallelism for environment compatibility
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Fit the topic model and transform the abstracts list
topic_model.fit_transform(english_abstracts_list)

# Retrieve and display the topic representation
list(topic_model.get_topic_info(0)['Representation'])

# Get and display the top topics information
topic_model.get_topic_info().head()

# Generate a DataFrame with document-topic information
doc_topics_df = topic_model.get_document_info(english_abstracts_list, df_abstracts)

# Display the last few entries of the document topics DataFrame
doc_topics_df.tail()

# Filter documents with high topic probability
topic_confident_df = doc_topics_df[doc_topics_df['Probability'] == 1]

# Prepare a list of abstracts with high topic confidence
abstract_list = []
for index, row in topic_confident_df.iterrows():
    data = {
        'corpusid': row['corpusid'],
        'abstract': row['abstract'],
        'Representation': row['Representation']
    }
    abstract_list.append(data)

# Define the base URL for DBpedia lookup
dbpedia_lookup = 'https://lookup.dbpedia.org/api/search?format=JSON&query='

# Query DBpedia for a subset of abstracts and store the results
abstract_list_dbpedia = []
for abstract in abstract_list[0:20]:
    keywords = ' '.join(abstract['Representation'])
    search_query = dbpedia_lookup + keywords
    query_result = requests.get(search_query).json()
    redirectlabel = query_result['docs'][0]['redirectlabel']
    label_cleaned = [label.replace("<B>", "").replace("</B>", "") for label in redirectlabel]
    abstract['dbpedia_query'] = label_cleaned
    abstract_list_dbpedia.append(abstract)
