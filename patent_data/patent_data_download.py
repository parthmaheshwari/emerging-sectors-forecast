import os
import requests
from tqdm import tqdm
from zipfile import ZipFile, BadZipFile
import zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

# Function to generate file names based on start and end years
def generate_file_names(start_year, end_year):
    file_names = []
    for year in range(start_year, end_year + 1):
        start_date = datetime.date(year, 1, 1)
        days_to_tuesday = (1 - start_date.weekday() + 7) % 7  # 1 is Tuesday
        tuesday = start_date + datetime.timedelta(days=days_to_tuesday)

        # Iterate through all Tuesdays of the year
        while tuesday.year == year:
            date_str = tuesday.strftime('%y%m%d')
            file_name = f"ipg{date_str}.zip"
            file_names.append(f"{year}/{file_name}")
            tuesday += datetime.timedelta(days=7)

    return file_names

start_year = 2005
end_year = 2022
filenames = generate_file_names(start_year, end_year)

# Create output directory for downloaded files
output_dir = 'fullpatentdata'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
base_url = 'https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/'

# Function to download files from the USPTO website
def download_file(file):
    try:
        full_url = base_url + file
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(full_url, headers=headers, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(output_dir, os.path.basename(file))
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=128):
                    f.write(chunk)
        else:
            print(f"Failed to download {file}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error downloading {file}: {e}")

# Download files using ThreadPoolExecutor for multiprocessing
with ThreadPoolExecutor(max_workers=30) as executor:
    results = list(tqdm(executor.map(download_file, filenames), total=len(filenames)))

# List of files that encountered errors during download
error_files = [
    # (List of error files)
]

# Downloading error files
for file in tqdm(error_files):
    download_file(file)

# Extracting and cleaning up zip files
for filename in tqdm(os.listdir(output_dir)):
    if filename.endswith(".zip"):
        zip_path = os.path.join(output_dir, filename)
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(output_dir)
            os.remove(zip_path)
        except zipfile.BadZipFile:
            print(f"Error: The file {filename} is not a valid zip file or is corrupted.")
