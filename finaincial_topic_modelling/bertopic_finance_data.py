"""
This Python script demonstrates the usage of the BERTopic library to perform topic modeling on a dataset of short descriptions.

It uses the following libraries:
- BERTopic: A library for topic modeling using BERT embeddings.
- pandas: A library for data manipulation and analysis.

The steps in the code are as follows:
1. Import necessary modules: BERTopic and pandas.
2. Read a CSV file containing organizational data with a column named "Investee Company Long Business Description\n('|')", or short.
3. Initialize a BERTopic model.
4. Perform topic modeling on the short descriptions from the dataset.
5. Retrieve the topics and their associated probabilities.
6. Print the topic information, including the topic IDs and their most representative terms.

Note: Make sure to specify the correct file path for the CSV file containing your dataset.

Usage:
- Run the script to perform topic modeling on the specified dataset and print topic information.
"""

import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer
from preprocessing.financial_preprocessor import preprocess_descriptions

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer

## Load preprocessed organizational data from a CSV file (adjust the file path as needed)
merged_df = pd.read_csv("datasets/unique_companies_processed_2000_2023.csv")

# Filter out US based tech companies
cs_data = merged_df[(merged_df["Company Nation"]=="United States")&(merged_df["Investee Company TRBC Industry Group\n('|')"]=="Software & IT Services")]

# drop rows that have either of the columns missing
cs_data = cs_data.dropna(axis=0, how='any', subset=["Investee Company Short Business Description\n('|')","Investee Company Long Business Description\n('|')","Company Name"])

## Initialize a BERTopic model
# Step 1 - Extract embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Step 2 - Reduce dimensionality
umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')

# Step 3 - Cluster reduced embeddings
hdbscan_model = HDBSCAN(min_cluster_size=5, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

# Step 4 - Tokenize topics
vectorizer_model = CountVectorizer(stop_words="english", preprocessor = preprocess_descriptions, ngram_range = (1,3))

# Step 5 - Create topic representation
ctfidf_model = ClassTfidfTransformer()

# Step 6 - (Optional) Fine-tune topic representations with 
# a `bertopic.representation` model
representation_model = KeyBERTInspired()

## All steps together
topic_model_ft_long = BERTopic(
  embedding_model=embedding_model,          # Step 1 - Extract embeddings
  umap_model=umap_model,                    # Step 2 - Reduce dimensionality
  hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
  vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
  ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
  representation_model=representation_model # Step 6 - (Optional) Fine-tune topic represenations
)

## Perform topic modeling(after fine tuning) on the long descriptions of organizations - To extract Topic predictions for each documents probabilities: The probability of the assigned topic per document
documents, probabilities = topic_model_ft_long.fit_transform(list(cs_data["Investee Company Long Business Description\n('|')"]))

## Print topic information for the top 50 topics
topics_long_ft = topic_model_ft_long.get_topic_info()
print(topic_model_ft.head(50))

# Save the generated topics
topics_long_ft.to_csv("topics_long_ft_5_all_data.csv")

# Save the topic model
topic_model_ft_long.save("topic_model_finetuned_long_5_full_data")