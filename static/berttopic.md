# BertTopic

BERTopic is a topic modeling technique that leverages BERT embeddings for clustering text data into various topics. It leverages Hugging-face transformers and c-TF-IDF to create dense clusters allowing for easy interpretation of topics and also keeping the important words from topic descriptions. It enables us to build our own topic model by utilizing the different types of sub-models.

## Inputs:
Documents: A list of texts that we want to group into topics. This could be sentences, paragraphs, or entire documents.

## BERTopic Algorithm:

The topic representation creation involves the following five step process.Every step is somewhat independent of one another.

## Embedding documents:

Embedding involves transforming the documents into numerical representation. BERTopic utilizes sentence-transformers by default to perform this step.These models excel in semantic similarity, aiding our clustering. In BERTopic, two default models are "all-MiniLM-L6-v2" (optimized for English semantic similarity) "paraphrase-multilingual-MiniLM-L12-v2" (supports 50+ languages, chosen for non-English languages). 

## Dimensionality reduction:  

Once we've numerically represented our documents, we need to reduce their dimensionality. Clustering struggles with high-dimensional data due to the curse of dimensionality. While there are methods like PCA, BERTopic defaults to UMAP. UMAP (Uniform Manifold Approximation and Projection) retains both local and global data structures during reduction, crucial for clustering semantically similar documents.


## Cluster documents:

After reducing our embeddings, we proceed to cluster our data using the density-based clustering method, HDBSCAN which is the default model used by BERTopic. This technique can detect clusters of varying shapes and has the capability to pinpoint outliers. Consequently, documents aren't wrongly categorized, leading to a clearer topic representation with minimal noise.

## Bag-of-Words:

Given that our chosen clustering method, HDBSCAN, is capable of identifying clusters with diverse densities and configurations, we recognize that a centroid-focused representation may fall short. As such, we strive for a strategy devoid of presumptions regarding the cluster's structure.To execute this, we consolidate all the documents within a single cluster into one comprehensive document, which then embodies that cluster. Subsequently, we compute the frequency of each word within the cluster. This process is known as bag-of-words representation.

## Topic representation:

The next step involves discerning the distinctions between clusters. For this, we adapt the TF-IDF to focus on topics rather than individual documents by using a class-based TF-IDF approach. Here, each cluster is treated as a singular document. We then determine the frequency of a word 'x' in a cluster 'c'. We derive a class-based tf representation, L1-normalized for topic size differences. Next, we calculate a modified idf using a logarithmic formula based on average word counts and word frequencies. By multiplying tf and idf, we obtain each word's importance within a cluster, using an optimized variant of the traditional TF-IDF.


## Fine-tune topic representation:

This optional step enhances the topics derived from c-TF-IDF using recent methods. With these techniques, topics can be further refined using tools like GPT, T5, KeyBERT, Spacy, among others. In bertopic.representation, the implemented models include:

MaximalMarginalRelevance
PartOfSpeech
KeyBERTInspired
ZeroShotClassification
TextGeneration
Cohere
OpenAI
LangChain.


### Research data BERTopic model parameters:

We sampled approximately 30,000 abstracts and utilized the BERTopic model to derive topic representations for each one. These representations were concatenated using spaces to construct a query string, which was then added to the dbpedia_lookup URL, forming a search query URL. The ensuing search outcomes were incorporated into the abstract dictionary under the key ‘dbpedia_query’ (only for the initial 20 abstracts).

The parameters set for the BERTtopic model are:

### Embedding Model: paraphrase-multilingual-MiniLM-L12-v2
Dimensionality Reduction: UMAP (15 neighbors, 5 components, using cosine similarity)
Clustering Method: HDBSCAN
Bag-of-Words Representation: CountVectorizer with English stop words
Topic Representation Technique: c-tf-idf
Fine-tuning Approach: Inspired by KeyBERT.

Sample output (Research data):
```json
{
    'corpusid': 250491760,
    'abstract': 'OBJECTIVES\nTo determine the predictive value of cardiac magnetic resonance (CMR) and echocardiographic parameters on left ventricular (LV) remodeling in ST-segment elevation myocardial infarction (STEMI) patients without cardiogenic shock and treated with mechanical LV unloading followed by immediate or delayed percutaneous coronary intervention (PCI)-mediated reperfusion.\n\n\nBACKGROUND\nIn STEMI, infarct size (IS) directly correlates with major cardiovascular outcomes. Preclinical models demonstrate mechanical LV unloading before reperfusion reduces IS. The door-to-unload (DTU)-STEMI pilot trial evaluated the safety and feasibility of LV unloading and delayed reperfusion in patients with STEMI.\n\n\nMETHODS\nThis multicenter, prospective, randomized, safety and feasibility trial evaluated patients with anterior STEMI randomized 1:1 to LV unloading with the Impella CP (Abiomed) followed by immediate reperfusion vs delayed reperfusion after 30 minutes of unloading. Patients were assessed by CMR at 3-5 days and 30 days post PCI. Echocardiographic evaluations were performed at 3-5 and 90 days post PCI. At 3-5 days post PCI, patients were compared based on IS as percentage of LV mass (group 1 ≤25%, group 2 >25%). Selection of IS threshold was performed post hoc.\n\n\nRESULTS\nFifty patients were enrolled from April 2017 to May 2018. At 90 days, group 1 (IS ≤25%) exhibited improved LV ejection fraction (from 53.1% to 58.9%; P=.001) and group 2 (IS >25%) demonstrated no improvement (from 37.6% to 39.1%; P=.55). LV end-diastolic volume and end-systolic volume were unchanged in group 1 and worsened in group 2. There was correlation between 3-5 day and 30-day CMR measurements of IS and 90-day echocardiography-derived LV ejection fraction.\n\n\nCONCLUSIONS\nImmediate 3-5 day post-therapy IS by CMR correlates with 90-day echocardiographic LVEF and indices of remodeling. Patients with post-therapy IS >25% demonstrated evidence of adverse remodeling. Larger studies are needed to corroborate these findings with implications on patient management and prognosis.',
    'Representation': ['cardiac',
        'ventricular',
        'myocardial',
        'coronary',
        'cardiovascular',
        'aortic',
        'ventricle',
        'echocardiography',
        'aorta',
        'arterial'
    ]
}
```








