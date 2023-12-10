# !pip install openpyxl
import os
import pandas as pd

def load_directory(directory_path):
    """
    Load data from multiple Excel files within a directory and combine them into a single DataFrame.

    Args:
        directory_path (str): The path to the directory containing Excel files to be loaded.

    Returns:
        pandas.DataFrame: A combined DataFrame containing data from all the Excel files in the directory.

    This function iterates through all the files in the specified directory and loads data from Excel files
    (with the assumption that they have the .xlsx file extension). It concatenates the loaded dataframes into
    a single combined dataframe, adding a 'year' column based on the year information extracted from the
    filenames. The resulting combined dataframe is returned.

    Example:
    >> data_directory = "/path/to/excel_files/"
    >> combined_data = load_directory(data_directory)
    >> print(combined_data.head())
    # Output: A combined DataFrame with data from all Excel files in the directory.
    """
    # Initialize an empty dataframe to store the combined data
    combined_df = pd.DataFrame()

    # Loop through files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.xlsx'):
            # Assuming your dataframes are in Excel files
            file_path = os.path.join(directory_path, filename)
            
            # Load each dataframe from Excel file and concatenate it to the combined dataframe
            df = pd.read_excel(file_path)
            
            # Extract the 'year' from the filename and add it as a new column in the dataframe
            df["year"] = int(filename.split("_")[2].split(".")[0])
            
            # Remove the last row (totals) if necessary
            df.drop(df.index[-1], inplace=True)
            
            # Concatenate the loaded dataframe to the combined dataframe
            combined_df = pd.concat([combined_df, df], ignore_index=True)

    return combined_df


# Define the directory where your company description dataframes (2011-2023) are stored
directory_path_company_info = 'datasets/company_info'
combined_df_info = load_directory(directory_path_company_info)
combined_df_info['Company Name'] = combined_df_info['Company Name'].fillna(combined_df_info['Investee Company Name'])
combined_df_info['Company Nation'] = combined_df_info['Company Nation'].fillna(combined_df_info['Investee Company Nation'])
temp_info = combined_df_info.sort_values('year', ascending=False).drop_duplicates('Company Name')
temp_info = temp_info[["Company Name","Investee Company Website\n('|')",
 "Investee Company Status\n('|')",
 "Investee Company Founded Date\n('|')",
 "Investee Company Long Business Description\n('|')",
 "Investee Company Short Business Description\n('|')",
 "Investee Company Alias Name\n('|')"]]


# Define the directory where company category information dataframes (2011-2023) are stored
directory_path_category_info = 'datasets/companies'
combined_df = load_directory(directory_path_category_info)
combined_df['Company Name'] = combined_df['Company Name'].fillna(combined_df['Investee Company Name'])
combined_df['Company Nation'] = combined_df['Company Nation'].fillna(combined_df['Investee Company Nation'])
temp = combined_df.sort_values('year', ascending=False).drop_duplicates('Company Name')

# Merge Company info and company categories (2011-2023)
merged_df = pd.merge(temp, temp_info, on='Company Name', how='left')

# Define the directory where vishal's dataframes containing both company info and category info from 2000-2010 are stored
directory_path_vishal = 'datasets/companies_vishal'
combined_df2 = load_directory(directory_path_vishal)
combined_df2.rename(columns = {"Investee Company Nation":"Company Nation","Investee Company Name":"Company Name"}, inplace=True)
combined_df2 = combined_df2.sort_values('year', ascending=False).drop_duplicates('Company Name')

# Ensuring that columns in both 2000-2010 and 2011-2023 datasets are same
merged_df.drop(columns = ['Investee Company Name', 'Investee Company Nation', 'No. of Deals in Search Range', 'No. of Firms in Search Range', 'No. of Funds in Search Range', 'Avg Deal Value in Search Range\n(USD, Millions)', 'Sum of Deal Value in Search Range\n(USD, Millions)', 'Sum of Deal Rank Value in Search Range\n(USD, Millions)'],inplace=True)
columns = list(merged_df)
combined_df2 = combined_df2[columns]

# Append both datasets 
merged_df = pd.concat([combined_df2,merged_df])
merged_df = merged_df.sort_values('year', ascending=False).drop_duplicates('Company Name').reset_index(drop=True)

# US only rows(optional)
merged_df = merged_df[merged_df["Company Nation"]=="United States"]

merged_df.to_csv("unique_companies_processed_2000_2023.csv")

# CS only rows(optional)
cs_data = merged_df[merged_df["Investee Company TRBC Industry Group\n('|')"]=="Software & IT Services"]
cs_data = cs_data.dropna(axis=0, how='any', subset=["Investee Company Short Business Description\n('|')","Investee Company Long Business Description\n('|')","Company Name"])

# Save dataset
cs_data.to_csv("tech_data_2000_2023.csv")