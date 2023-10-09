"""
This Python script demonstrates the usage of the BERTopic library to perform topic modeling on a dataset of short descriptions.

It uses the following libraries:
- BERTopic: A library for topic modeling using BERT embeddings.
- pandas: A library for data manipulation and analysis.

The steps in the code are as follows:
1. Import necessary modules: BERTopic and pandas.
2. Read a CSV file containing organizational data with a column named "short_description." The 'nrows' parameter limits the number of rows read to 10,000,000.
3. Initialize a BERTopic model.
4. Perform topic modeling on the short descriptions from the dataset.
5. Retrieve the topics and their associated probabilities.
6. Print the topic information, including the topic IDs and their most representative terms.

Note: Make sure to specify the correct file path for the CSV file containing your dataset.

Usage:
- Run the script to perform topic modeling on the specified dataset and print topic information.
"""

from bertopic import BERTopic
import pandas as pd

# Load organizational data from a CSV file (adjust the file path as needed)
cb_data = pd.read_csv("datasets/organizations.csv", nrows=10000000)

# Initialize a BERTopic model
topic_model = BERTopic()

# Perform topic modeling on the short descriptions of organizations - To extract Topics
topics, probs = topic_model.fit_transform(list(cb_data["short_description"])[:10000])

# Print topic information for the top 50 topics
print(topic_model.get_topic_info().head(50))