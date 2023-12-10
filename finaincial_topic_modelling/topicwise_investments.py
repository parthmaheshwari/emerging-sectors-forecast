import os
import pandas as pd
from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer

# Function to merge data for each topic and include years and fill missing values
def fill_missing_years(x):
    """
    Merge data for each topic to include years and fill missing values.
    
    Args:
        x (DataFrame): Dataframe for a specific topic.
        
    Returns:
        DataFrame: Merged and processed DataFrame for the topic.
    """
    out = x.merge(
        pd.Series(range(2001, 2024), name="investment_year"),
        how="right",
    )
    out["Topic"] = x.name
    out['Deal Rank Value\n(USD, Millions)'] = out['Deal Rank Value\n(USD, Millions)'].fillna(0)
    return out

# Specify the folder where your datasets are located
folder_path = 'datasets/investments'

# Initialize an empty list to store DataFrames
dfs = []

# Loop through the files in the folder
for filename in os.listdir(folder_path):
    print(filename)
    if filename.endswith('.xlsx'):  # Adjust the file extension as needed
        file_path = os.path.join(folder_path, filename)
        # Read the Excel file into a DataFrame and append it to the list
        df = pd.read_excel(file_path)
        df["investment_year"] = filename.split("_")[0]
        dfs.append(df.iloc[:-1])  # Exclude the last row if necessary

# Concatenate all DataFrames in the list into one final DataFrame
final_dataframe = pd.concat(dfs, ignore_index=True)
final_dataframe = final_dataframe.drop_duplicates()

# Remove duplicate rows based on all columns except 'Firm Investor Name' and 'Fund Investor Name'
# this is an important step, to ensure that funding amount is not duplicated across multiple investors
final_dataframe = final_dataframe.drop_duplicates(subset=final_dataframe.columns.difference(['Firm Investor Name','Fund Investor Name']))

# Load topic data from a CSV file
long_topics = pd.read_csv("topics_long_ft_5_all_data.csv")

# Load the pre-trained BERTopic model
topic_model_ft_long = BERTopic.load("topic_model_finetuned_long_5_full_data")

# Read data about unique companies from a CSV file
merged_df = pd.read_csv("unique_companies_processed_2000_2023.csv")

# Filter companies in the "Software & IT Services" industry
cs_data = merged_df[merged_df["Investee Company TRBC Industry Group\n('|')"]=="Software & IT Services"]

# Remove rows with missing values in specified columns
cs_data = cs_data.dropna(axis=0, how='any', subset=["Investee Company Short Business Description\n('|')","Investee Company Long Business Description\n('|')","Company Name"]).reset_index()

# Extract topic information for the selected long descriptions
topic_df = topic_model_ft_long.get_document_info(list(cs_data["Investee Company Long Business Description\n('|')"]), df=cs_data[["Company Name","Investee Company Long Business Description\n('|')"]], metadata=None)
topic_df = topic_df[topic_df["Topic"]!=-1]

# Merge data about companies and their financial investments with topic information
merged_df = pd.merge(final_dataframe, topic_df, left_on="Investee Company Name", right_on="Company Name", how="inner")

# Convert the "investment_year" column to integers
merged_df["investment_year"] = merged_df["investment_year"].astype(int)

# Group data by topic and investment year, applying the 'fill_missing_years' function to each group
grouped = merged_df.groupby("Topic").apply(fill_missing_years).reset_index(drop=True)

# Group data by 'Topic' and 'investment_year' to calculate the sum of 'Deal Rank Value\n(USD, Millions)' for each group
sums = grouped['Deal Rank Value\n(USD, Millions)'].sum()

# Create a DataFrame with the sums and save it to a CSV file
grouped_investment_df = sums.reset_index()
grouped_investment_df.to_csv("yearwise_topicwise_investments_2000_2023.csv")
