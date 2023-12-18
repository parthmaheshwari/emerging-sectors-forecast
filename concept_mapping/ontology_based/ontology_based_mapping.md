# Ontology Based Mapping

## Introduction
In Ontology based mapping we leverage a predefined hierarchical ontology to build a mapping. We are leveraging [OpenAlex Ontology](https://docs.google.com/spreadsheets/d/1LBFHjPt4rj_9r0t0TTAlT68NwOtNH8Z21lBMsJDMoZg/edit#gid=575855905) in our usecase.

## Method
Below are the detailed steps of the process
- We first tag all the documents in our data with concepts from the Ontology. OpenAlex provides a scalable concept tagger for the purpose.
- All the concepts that come under a particular concept in the hierarchical ontology are considered to be related to that concept.
- Given the input concept:
    1. We find all the children concepts (till the leaf nodes) using depth-first search.
    2. This collection of concepts serve as an exhaustive representation of the input concept.
    3. We search for these concepts in our data and any document which has any of these concepts serves as a relevant document for our usecase. 

## Scripts Descriptions
1. Concept Tagging
    - For tagging concepts we first deploy the openalex-concept-tagger V3 model on our local/server machine. The steps and the script are mentioned in the folder openalex-concept-tagging .
    - the script tag_concepts_finance.py takes in a jsonl file path and batch_size as input arguments. 
