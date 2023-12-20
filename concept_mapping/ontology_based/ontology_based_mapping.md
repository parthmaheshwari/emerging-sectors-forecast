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
All the scripts work on a list of json files. 
1. concept_tagging_utilities.py : has all the requred functions to get concepts tagged from openalex concept tagger
2. concept_tagging_academic_data.py : this script is used to tag concepts on academic data. It uses "corpusid" as the unique document identifier by default. It also used title and abstract from the documents to get the concepts.
3. concept_tagging_patent_data.py : this script is used to tag concepts to patent data. It uses a "created_unque_id" as a unique document identifier. Moreover, for concept tagging it uses 'invention-title' and 'abstract' fields.
4. concept_tagging_finance_data.py : this script is used for tagging concepts in finance data. The finance data is in a pandas dataframe so first it should be converted to a jsonl file. Each jsonl object should have unique identifier key, short_description and long_description keys.
