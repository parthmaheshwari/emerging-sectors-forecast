import random
random.seed(123)

import re
import time
import os
import ast
import requests
import json
import jsonlines
import numpy as np
import pandas as pd
from tqdm import tqdm
import urllib.parse, urllib.request

from concept_tagging_utilities import batch_items, get_concept_tagged_dict_from_tagger
from concept_tagging_utilities import prepare_json_for_patent_data


if __name__ == "__main__":

    # Unique identifier key name in the data
    unique_key_in_data = 'created_unique_id'

    # enter the path of the jsonl files folder
    main_path_of_data = ''

    all_data_files = sorted([os.path.join(main_path_of_data, f) for f in os.listdir(main_path_of_data)])

    print('Total files to be processed are : {}'.format(len(all_data_files)))

    for fileidx, filepath in enumerate(all_data_files):
        print("File idx : {}   |  File : {}".format(fileidx, filepath))
        
        all_data = []
        with jsonlines.open(filepath, 'r') as reader:
            for item in tqdm(reader):
                all_data.append(item)

        input_data_for_concept_tagger = prepare_json_for_patent_data(all_data, unique_key_in_data=unique_key_in_data)
        print(f'Total number of records to be tagged in file are : {len(input_data_for_concept_tagger)}')

        # Group items into batches of 8
        batched_items = list(batch_items(input_data_for_concept_tagger, batch_size=8))

        output = []
        # Print the batched items
        for batch in tqdm(batched_items, total=len(batched_items)):
            output.append(get_concept_tagged_dict_from_tagger(batch))

        all_data_dict = {
            item[unique_key_in_data]: item 
            for item in all_data
        }
        
        for out_item in tqdm(output):
            for o_item in out_item:
                all_data_dict[o_item['work_id']]['openalex_concept_ids']  = o_item['tag_ids_without_chains']
                all_data_dict[o_item['work_id']]['openalex_concept_ids_with_full_chain']  = o_item['tag_ids']
                all_data_dict[o_item['work_id']]['openalex_concepts']  = o_item['tags_without_chains']
                all_data_dict[o_item['work_id']]['openalex_concepts_with_chains']  = o_item['tags']

        with jsonlines.open(filepath, 'w') as writer:
            for _, val in tqdm(all_data_dict.items()):
                writer.write(val)
        
        time.sleep(10)