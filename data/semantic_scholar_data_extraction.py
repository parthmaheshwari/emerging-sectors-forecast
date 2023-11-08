"""
This Python script downloads datasets from Semantic Scholar using concurrent processing for speed.
It automatically downloads the following data types: research papers, their abstracts, author information, and summaries.
The script uses multiple threads to speed up the download and extraction process.

You can add more dataset types if needed. Please make sure to use your Semantic Scholar API key by 
replacing 'YOUR_API_KEY_HERE' with your actual API key or by using an environment variable to store it.


To run this script, type the following in your terminal:
    python semantic_scholar_data_extraction.py
    
"""



import os
import requests
import gzip
import shutil
import concurrent.futures

# Replace 'YOUR_API_KEY_HERE' with your actual API key.
headers = {
    'API_KEY': 'YOUR_API_KEY_HERE'
}

def extract_file(file_url, file_type, index):
    """
    Generalized file extraction function for various file types from Semantic Scholar.
    """
    zipped_folder = f'zipped_{file_type}'
    unzipped_folder = f'unzipped_{file_type}'
    
    if not os.path.exists(zipped_folder):
        os.makedirs(zipped_folder)
    if not os.path.exists(unzipped_folder):
        os.makedirs(unzipped_folder)

    file_name = os.path.join(zipped_folder, f'{file_type}_{index}.gz')
    
    # Stream the file download and write it to a gz file
    with requests.get(file_url, stream=True, headers=headers) as response:
        with open(file_name, 'wb') as output:
            for chunk in response.iter_content(chunk_size=8192):
                output.write(chunk)
    
    # Unzip the gz file and write its contents to a new file
    with gzip.open(file_name, 'rb') as f_in:
        unzipped_file_name = os.path.join(unzipped_folder, f'{file_type}_{index}')
        with open(unzipped_file_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def download_and_extract(data_type):
    """
    Download and extract data files for a specific type from Semantic Scholar.
    """
    api_url = f'https://api.semanticscholar.org/datasets/v1/release/latest/dataset/{data_type}'
    data_info = requests.get(api_url, headers=headers).json()
    data_files = data_info['files']

    with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
        futures = [executor.submit(extract_file, file_url, data_type, index) for index, file_url in enumerate(data_files)]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result() 
            except Exception as e:
                print(f"Exception occurred during {data_type} download: {e}")

def main():
    # You can add any additional data types you want to download in this list
    data_types = ['papers', 'abstracts', 'authors', 'tldrs']
    for data_type in data_types:
        print(f"Downloading and extracting {data_type}...")
        download_and_extract(data_type)

if __name__ == "__main__":
    main()

