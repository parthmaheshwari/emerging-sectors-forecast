"""
This script processes and merges academic paper and abstract data from the Semantic Scholar dataset.
It extracts relevant fields from the downloaded JSON files, including corpus ID, year, title, 
authors, reference count, citation count, and abstracts. The script is designed to work with 
data from a specific category, which is passed as a parameter. The final output is a consolidated 
JSON file containing all the required information for each paper in the specified category.
"""

import json
import os

def process_papers(line, category):
    """
    Process each line of the input JSON file and extract required fields for papers in the specified category.
    """
    paper = json.loads(line)
    data = {
        'corpusid': paper.get('corpusid', None),
        'year': paper.get('year', None),
        'title': paper.get('title', None),
        'authors': paper.get('authors', None),
        'referencecount': paper.get('referencecount', None),
        'citationcount': paper.get('citationcount', None)
    }

    if 's2fieldsofstudy' in paper and isinstance(paper['s2fieldsofstudy'], list):
        for field in paper['s2fieldsofstudy']:
            if field.get('category') == category:
                return data  
    return None

def main(category):
    # Define input directories
    papers_directory = '/Semantic_Scholar/unzipped_papers'
    abstracts_directory = '/Semantic_Scholar/unzipped_abstracts'

    # Process papers in the specified category
    cse_papers_data = []
    for file in os.listdir(papers_directory):
        file_path = os.path.join(papers_directory, file)
        with open(file_path, 'r', encoding='utf-8') as jsonl_file:
            for line in jsonl_file:
                extracted_data = process_papers(line, category)
                if extracted_data:
                    cse_papers_data.append(extracted_data)

    # Create dictionary for quick access
    cse_papers_dict = {paper['corpusid']: paper for paper in cse_papers_data}

    # Process abstracts
    for file in os.listdir(abstracts_directory):
        file_path = os.path.join(abstracts_directory, file)
        with open(file_path, 'r', encoding='utf-8') as jsonl_file:
            for line in jsonl_file:
                abstract = json.loads(line)
                corpusid = abstract.get('corpusid', None)
                if corpusid in cse_papers_dict:
                    cse_papers_dict[corpusid]['abstract'] = abstract.get('abstract', None)

    # Convert dictionary back to list
    cse_papers_dict_updated = list(cse_papers_dict.values())

    # Save the merged data
    with open(f'{category}_papers_integrated_data.json', 'w') as f:
        json.dump(cse_papers_dict_updated, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process and merge academic paper data for a specific category.")
    parser.add_argument("category", type=str, help="The category of papers to process (e.g., 'Computer Science')")
    args = parser.parse_args()

    main(args.category)
