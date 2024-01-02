# Concept Mapping

## Introduction
We tried two approaches for preparing a cross domain mapping. We initially build an embedding based cross domain mapping leveraging topic modelling. Finally, we used an open source ontology, namely OpenAlex Ontology, to build this mapping. More detailed information about both the methods is provided in the below sections. 


## Embedding Based Mapping
Here, we leverage the topic models to identify topics from different domains. We also assume the topics in academic domain to be much larger than the finance domain. So, topics from academic domain are mapped to the finance domain. The steps are mentioned below :
- Each topic is a collection of words. We leveraged GPT-3.5-turbo to get human interpretable label for each topic from both finance and academic domains.
- For every topic we use the collection of its words to get the vector representation using **text-embedding-ada-002** model from OpenAI. 
- The mapping is created using the below steps:
    1. For every Finance topic, we calculate the cosine similarity with every Academic Topic.
    2. Sort the Academic Topics according to the cosine similarity scores with the Finance Topic.
    3. All academic topics which have
        - cosine similarity greater than 0.8
        - a difference of less than 0.03 with previously mapped academic topic.
4. The above process is repeated for every finance topic, resulting in a list of academic topics for every finance topic. 

For example : one of the topics identified in Finance data is **Artificial Intelligence** and using the embedding based mapping we get the mapped academic topics as : **Spiking Neural Networks, Artificial Intelligence, Automation and Human Factors, Business Intelligence, Intelligent Tutoring Systems, Brain Connectivity, Robotics, Brain-Computer Interfaces, Chatbot and Conversational Agents**.


## Ontology Based Mapping
Here, rather than generating a mapping ourselves we leverage an open source hierachical ontology from **OpenAlex**. However, using this ontology meant to tag all the text data with concepts from the ontology only and the developed topic models were of no use. 

Given any concept we travel down in the ontology to the leaf nodes throguh the children of each node using depth first search. In this way a concept is expanded into a list of related concepts using the ontology.

### OpenAlex Ontology 
It is derived from MAG and consists of 65K concepts divided into 6 levels. Level 0 means disciplines for example Physics, Computer Science etc. and with every increasing level the granularity increases with leaf nodes at level 5. Level 0 has 10 concepts and Level 1 has 294 concepts, all are manually decided.


### OpenAlex Concepts Tagging
For concept tagging OpenAlex has provided a scalable solution that can be deployed using AWS or on a local machine. More details in the ontology_based sub folder. The steps for setting up the tagger or local are mentioned below:
1. Clone the [OpenAlex ConcepTagger Github](https://github.com/ourresearch/openalex-concept-tagging) and go in the cloned repo. 
2. Download the model artifacts using 
```python
aws s3 cp s3://openalex-concept-tagger-model-files/ . --recursive
```
  3. Follow the this [link](https://github.com/ourresearch/openalex-concept-tagging/tree/main/V3) to download and set up open alex concept tagger.
  4. Create a separate folder "V3" inside "V3/003_Deploy/model_to_api/container/" for saving the model weights and vocabularies.
  5. Download and set up the required conda environment [py38_with_gpu](https://drive.google.com/file/d/1zsDwyl6WydDjcxWTZcEXJOq9iT7zGPtA/view?usp=sharing) or [py38_without_gpu](https://drive.google.com/file/d/1kVPZ93j_XiZUvUsZ9TBiQqi7fvzasSg3/view?usp=sharing)
  6. Run the predictor script at V3/003_Deploy/model_to_api/container/mag_model/predictor.py
