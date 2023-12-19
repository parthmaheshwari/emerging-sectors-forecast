# BERTopic Tutorial on Academic Data

## Introduction
In this approach, we explore the intersection of academic research and private finance equity firms using advanced topic modeling techniques. By employing BERTopic for extracting topics from academic texts and financial narratives, and then fusing these insights with embeddings, we aim to illuminate the influence of academic trends on the finance sector. This approach harnesses the deep language understanding of both BERTopic and deep language processing, offering a unique perspective on how academic developments can shape financial strategies and decisions.

BERTopic is ideal for academic data due to its deep understanding of context, crucial for processing complex and specialized academic language. It efficiently handles large, diverse datasets typical in academia and dynamically adapts to evolving research terminologies, offering more accurate and coherent topic extraction. Additionally, BERTopic's ability to produce high-quality, distinct topics and integrate with other NLP tools makes it a valuable asset for academic research analysis.

## Setting Up the Environment

```bash
pip install bertopic
pip install umap-learn
pip install hdbscan
```
## Data Preparation

The dataset for topic modeling is extracted using the academic_papers_data_integrator.py script located in the preprocessing directory. This script processes academic data and structures it for analysis.

To display a sample of your data in Markdown format (as used on GitHub), you can use a code block to ensure it's properly formatted and easy to read. Here's how you can present the sample data in your README.md or other Markdown documents on GitHub:

markdown

### Sample Data 

Below is a sample entry from the dataset obtained using the `academic_papers_data_integrator.py` script:

```json
{'corpusid': 63264242,
 'year': 2016,
 'title': 'Mathematical Foundation Of Parallel Computing',
 'authors': [{'authorId': '46675155', 'name': 'S. Hirsch'}],
 'referencecount': 0,
 'citationcount': 0,
 'abstract': 'Thank you for reading mathematical foundation of parallel computing. As you may know, people have search hundreds times for their chosen books like this mathematical foundation of parallel computing, but end up in harmful downloads. Rather than enjoying a good book with a cup of coffee in the afternoon, instead they cope with some harmful virus inside their laptop. mathematical foundation of parallel computing is available in our book collection an online access to it is set as public so you can get it instantly. Our book servers spans in multiple locations, allowing you to get the most less latency time to download any of our books like this one. Kindly say, the mathematical foundation of parallel computing is universally compatible with any devices to read.'}
```


### Preprocessing
BERTopic is robust enough to handle raw data effectively. However, to optimize the quality of the topic modeling, we perform basic preprocessing on the abstracts. This preprocessing ensures the data is clean and standardized, enhancing the model's ability to accurately identify and categorize topics.

The preprocessing involves:

1. **Removing HTML Tags, URLs, and Non-Alphabetic Characters:** 
   - Cleans the abstracts by removing HTML tags, web URLs, and non-alphabetic characters.

2. **Converting Text to Lowercase:** 
   - Standardizes all text to lowercase, important for consistent NLP processing.

3. **Eliminating Extra Spaces:** 
   - Removes any formatting issues by reducing multiple spaces to a single space.

Here is the Python function for the preprocessing:

```python
import re
def preprocess_abstracts(abstract):
    """
    Preprocess the abstracts by removing HTML tags, URLs, non-alphabetic characters, and extra spaces.
    The text is also converted to lowercase.
    """
    # Remove HTML tags
    abstract = re.sub(r'<.*?>', ' ', abstract)
    
    # Remove URLs
    abstract = re.sub(r'http\S+|www\S+|https\S+', ' ', abstract, flags=re.MULTILINE)
    
    # Keep only alphabetic characters
    abstract = re.sub(r'[^a-zA-Z\s]', ' ', abstract)
    
    # Convert to lowercase and remove extra spaces
    abstract = re.sub('\s+', ' ', abstract).lower()
    
    return abstract
```

```python
processed_abstracts = [preprocess_abstracts(paper['abstract']) for paper in papers]
```

## Using BERTopic

After preprocessing and preparing our data, we move on to using BERTopic for topic modeling. BERTopic leverages transformers and c-TF-IDF to create dense clusters, allowing for easily interpretable topics.

### Choosing SPECTER for Academic Data

For embedding our academic dataset, we opt for the SPECTER model (`'sentence-transformers/allenai-specter'`). SPECTER, or Scientific Paper Embeddings using Citation-informed Transformers, is specifically tailored to grasp the nuanced semantic content of scientific literature. It leverages the citation context, making it adept at understanding complex academic discussions. This characteristic of SPECTER ensures more accurate and relevant topic extraction from scholarly articles.

### BERTopic Configuration
We configure BERTopic with various specialized models to enhance its performance on academic data:

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from custom_transformers import ClassTfidfTransformer, KeyBERTInspired

# Embedding model
embedding_model = SentenceTransformer('sentence-transformers/allenai-specter')

# UMAP model for dimensionality reduction
umap_model = UMAP(n_neighbors=10, n_components=5, min_dist=0.0, metric='cosine')

# HDBSCAN model for clustering
hdbscan_model = HDBSCAN(min_cluster_size=10, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

# CountVectorizer for vectorization
vectorizer_model = CountVectorizer(ngram_range=(1, 3), stop_words='english')

# Class-based TF-IDF transformer
ctfidf_model = ClassTfidfTransformer()

# KeyBERTInspired model for topic representation
representation_model = KeyBERTInspired()

# Creating the BERTopic instance
topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    hdbscan_model=hdbscan_model,
    vectorizer_model=vectorizer_model,
    ctfidf_model=ctfidf_model,
    representation_model=representation_model
)

```

In this setup, each component of BERTopic is carefully chosen to enhance the topic modeling process:

In our BERTopic setup, each component is strategically selected to optimize the topic modeling process:

- **UMAP (Uniform Manifold Approximation and Projection):** Used for dimensionality reduction to condense the feature space while retaining the structure of the data.
- **HDBSCAN (Hierarchical Density-Based Spatial Clustering of Applications with Noise):** Employed for clustering the data points (reduced dimensions) into meaningful topics.
- **CountVectorizer and ClassTfidfTransformer:** These are used for vectorization, converting text data into numerical format that can be processed by the model.
- **KeyBERTInspired Representation Model:** Customized for topic representation to enhance the interpretability of the topics.

While BERTopic is highly flexible and allows for various configurations. Depending on dataset and specific requirements, you can experiment with different modeling processes and configurations.

For more detailed information on how to configure and use BERTopic, including exploring other modeling options, visit the [BERTopic Algorithm Documentation](https://maartengr.github.io/BERTopic/algorithm/algorithm.html).


## Topic Extraction and Interpretation

After configuring BERTopic, the next step is to extract topics from the dataset:

```python
topics, probabilities = topic_model.fit_transform(processed_abstracts)
```

### Example of Extracted Topics
After running BERTopic, you might get a list of topics, each represented by a set of keywords. Here's an example of what these topics could look like:

- **Topic 1**: 'process', 'framework', 'developed', 'approach', 'research', 'study', 'proposed', 'various', 'results', 'management'

- **Topic 2**: 'biology', 'genomic', 'bioinformatics', 'gene expression', 'genes', 'gene', 'high throughput', 'genome', 'mutations', 'gene expression data'

- **Topic 3**:  'wireless sensor networks', 'wireless sensor network', 'sensor networks wsns', 'sensor nodes', 'sensor networks wsn', 'sensor network', 'sensor networks', 'sensor node', 'sensor network wsn', 'wireless sensor'

- **Topic 4**: 'software testing', 'software development', 'software engineering', 'software maintenance', 'software quality', 'quality software', 'software process', 'software architecture', 'software product', 'software products'

  
Identified Topics for a Sample Paper:

```json
{'corpusid': 63264242,
 'year': 2016,
 'title': 'Mathematical Foundation Of Parallel Computing',
 'authors': [{'authorId': '46675155', 'name': 'S. Hirsch'}],
 'referencecount': 0,
 'citationcount': 0,
 'abstract': 'Thank you for reading mathematical foundation of parallel computing. As you may know, people have search hundreds times for their chosen books like this mathematical foundation of parallel computing, but end up in harmful downloads. Rather than enjoying a good book with a cup of coffee in the afternoon, instead they cope with some harmful virus inside their laptop. mathematical foundation of parallel computing is available in our book collection an online access to it is set as public so you can get it instantly. Our book servers spans in multiple locations, allowing you to get the most less latency time to download any of our books like this one. Kindly say, the mathematical foundation of parallel computing is universally compatible with any devices to read.',
 'Representation': ['parallel programming',
  'high performance computing',
  'massively parallel',
  'performance parallel',
  'data parallel',
  'parallel applications',
  'parallel program',
  'parallel application',
  'shared memory',
  'multicore']}

```



