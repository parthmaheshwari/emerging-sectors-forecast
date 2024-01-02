'''
This method used embeddings for topics from OpenAI api. Using cosine \
similarity the topics from Research Domain are mapped to Finance domain.
f
'''

import random
random.seed(123)

import ast
import os
import re
import time
import openai
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter


def get_completion(prompt):
    messages = [
        {
            'role': 'user',
            'content': prompt
        }
    ]
    response = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages=messages,
        temperature=0.2
    )
    return response.choices[0].message['content']


def get_output_from_api(input_prompt, max_tries=5):
    flag = False
    curr_tries = 0
    output = 'run_again'
    while flag == False:
        try :
            output = get_completion(input_prompt)
            flag = True
        except:
            time.sleep(20)
            print('Trying for the {} time'.format(curr_tries))
            if curr_tries >= max_tries:
                flag = True
            curr_tries += 1
    return output


def get_embedding_from_api(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
    return response


def get_topic_embedding(data):
    for item in data:
        word_list = item['representation']
        text = 'The text is discussing about ' + ', '.join(word_list[:-1]) + ' and {} topics.'.format(word_list[-1])
        text = re.sub('\s+', ' ', text)
        embedding = np.array(get_embedding_from_api(text))
        item['topic_embedding'] = embedding.tolist()
    return data


def get_phrase_labels_from_api(data):
    for item in data:
        word_list = item['representation']
        text = ', '.join(word_list)
        prompt = """
You are a Topic Model. You can identify the broad concepts given the list of words from a topic model.
Given the list of keywords, identify the Phrase label to represent the broad concept of the words in the list.
Provide the answer in a json format with "phrase_label" as key

        """.format(text)
        output = get_output_from_api(prompt)
        item['gpt_phrase_label'] = output['phrase_label']
    return data

def get_n_most_similar_topics_using_embeddings(query_topic_emb, topic_matrix, matrix_topic_names, topk=3):
    query_topic_emb = query_topic_emb.reshape(1,-1)
    similarity_with_research_topics = cosine_similarity(query_topic_emb, topic_matrix).tolist()[0]
    most_relevant_indices = np.argsort(similarity_with_research_topics)[-topk:][::-1]    
    most_relevant_topics = [p for p in  np.take(matrix_topic_names, most_relevant_indices).tolist()]    
    scores = np.sort(similarity_with_research_topics)[-topk:][::-1].tolist()
    return most_relevant_topics, most_relevant_indices, scores


def select_topics_to_be_mapped(inp_topic_names, inp_topic_indices, inp_topic_scores, min_score_limit=0.80, score_selection_limit=0.02):
    selected = []
    best_score = 0.0
    for name, index, score in zip(inp_topic_names, inp_topic_indices, inp_topic_scores):
        if score >= min_score_limit:
            if score > best_score:
                best_score = score
            
            if best_score - score <= score_selection_limit:
                selected.append(
                    {
                        'topic_id': int(index),
                        'topic_name': name,
                        'topic_similarity_score': float(round(score, 4))
                    }
                )
    return selected

if __name__ == "__main__":
    # load the research data 
    research_topics = json.load(open('research topic json file', 'r'))

    # add phrase labels
    research_topics = get_phrase_labels_from_api(research_topics)
    # add embeddings 
    research_topics = get_embedding_from_api(research_topics)

    # load the finance data 
    finance_topics = json.load(open('finance topic json file', 'r'))

    # add phrase labels
    finance_topics = get_phrase_labels_from_api(finance_topics)
    # add embeddings 
    finance_topics = get_embedding_from_api(finance_topics)

    # creating mapping 
    research_topic_embeddings_array = np.array(
        [i['topic_embedding'] for i in research_topics]
    )
    research_topic_phrase_labels = [
        i['gpt_phrase_label'] for i in research_topics
    ]

    for fin_item in finance_topics:
        fin_topic_name = fin_item['gpt_phrase_label']
        fin_topic_embedding = np.array(fin_item['topic_embedding'])
        fin_topic_words = fin_item['representation']
        
        # print('Fin Topic == {}'.format(fin_topic_name))
        # print('Fin Topic words == {}'.format(fin_topic_words))
        # print()
        res_topic_names, res_topic_indices, res_topic_scores = get_n_most_similar_topics_using_embeddings(
            fin_topic_embedding, research_topic_embeddings_array, 
            research_topic_phrase_labels, topk=10
        )
        mapped_topics = select_topics_to_be_mapped(res_topic_names, res_topic_indices, res_topic_scores)
        fin_item['mapped_research_topics'] = mapped_topics
        
    #     for to, sc in zip(res_topic_names[:5], res_topic_scores[:5]):
    #         print('Research Topic Name : {}  | Similarity Score : {}'.format(to, sc))
            
    #     print('\n\n')