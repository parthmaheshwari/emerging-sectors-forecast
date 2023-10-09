import os
import pandas as pd

"""
This Python script combines multiple dataframes stored in Excel files within a specified directory into a single dataframe. It assumes that the dataframes are organized by year in the file names.

It uses the following libraries:
- os: A standard library for interacting with the file system.
- pandas: A library for data manipulation and analysis.
- openpyxl: A library for working with Excel files (requires installation).

The steps in the code are as follows:
1. Import the necessary modules: os and pandas.
2. Define the directory path where your Excel files containing dataframes are stored.
3. Initialize an empty dataframe called 'combined_df' to store the combined data.
4. Loop through files in the specified directory.
    a. Check if a file has a '.xlsx' extension (assuming dataframes are in Excel format).
    b. Construct the full file path for each dataframe.
    c. Load each dataframe from the Excel file and add a 'year' column extracted from the file name.
    d. Remove the last row of each dataframe (you may customize this step as needed).
    e. Concatenate the loaded dataframe with 'combined_df' to combine the data.
5. After the loop, 'combined_df' contains the merged data from all dataframes in the directory.

Note: Ensure that the 'openpyxl' library is installed to work with Excel files.

Usage:
- Replace 'directory_path' with the path to your directory containing Excel files.
- Customize the loading and preprocessing steps as needed based on your data format.
- Run the script to combine the data from multiple Excel files into a single dataframe.
"""

# requires openpyxl installation

# Define the directory where your dataframes are stored
directory_path = 'datasets/companies'

# Initialize an empty dataframe to store the combined data
combined_df = pd.DataFrame()

# Loop through files in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.xlsx'):  # Assuming your dataframes are in CSV files
        file_path = os.path.join(directory_path, filename)
        
        # Load each dataframe and concatenate it to the combined dataframe
        df = pd.read_excel(file_path)
        df["year"] = int(filename.split("_")[0])
        df.drop(df.index[-1], inplace=True)
        combined_df = pd.concat([combined_df, df], ignore_index=True)

# Now combined_df contains all the data from the dataframes in the directory