# Predicting Funding Flows in Public and Private Markets

## Overview
This GitHub repository contains the culmination of months of intensive research, analysis, and collaboration by a team of four students pursuing their Master of Science in Data Science at Michigan State University under the expert guidance of Professor Mohammad Ghassemi.

## Project Description
The world of finance is characterized by ever-shifting dynamics, where investors and decision-makers strive to anticipate market trends and make informed decisions. Predicting funding flows is a critical aspect of this process, as it can offer invaluable insights into market sentiment, economic conditions, and investment opportunities.

Our project aims to provide a robust framework for forecasting funding flows in public and private markets by harnessing the power of data science, time series analysis, and NLP. We understand that predicting funding flows is a challenging task due to the multifaceted nature of market data and the influence of external factors. However, we believe that a combination of advanced data analysis and machine learning techniques can help us make significant strides in this domain.

## Dataset
### Data Collection
We have collected data from various sources encompassing both open and proprietary datasets. In the academic domain, our sources include well-known repositories like Arxiv, S2ORC, and Crossref. In the financial domain, we have accessed data from Refinitive Workspace, Pitchbook, Crunchbase, and others.

For a comprehensive list of the datasets we have explored and detailed information about their features, please refer to the table available in [Datasets](static/datasets.md).

After conducting a thorough analysis of these datasets, taking into account factors such as feature richness and data update frequency, we have made the strategic decision to primarily utilize S2ORC for academic data, which comprises an extensive collection of research papers.To facilitate the collection of academic data from S2ORC, we have developed a Python script that uses concurrent processing for efficient data extraction.

1. Obtain a Semantic Scholar API key and replace `'YOUR_API_KEY_HERE'` with your actual API key in the script.
2. Run the script in your terminal:

```bash
cd data
python academic_data_extraction.py
cd ../preprocessing
python academic_data_integrator.py 'Computer Science'
```


Additionally, we have chosen to incorporate data from Refinitive Workspace to provide comprehensive coverage of the financial domain. The resources used to collect these two datasets are provided in the aforementioned Datasets table.


In addition to academic and financial datasets, our collection also includes granted patent data, sourced directly from the United States Patent and Trademark Office (USPTO). The USPTO, a federal agency of the Department of Commerce, is responsible for issuing patents for inventions and registering trademarks. This dataset comprises raw text from granted patents between 1976 till date, providing a rich source of information on technological advancements and intellectual property trends recognized by the USPTO over these years.

To extract patent data spanning from 2005 to 2023, follow these steps using the scripts located in the `patent_data` directory:

1. **Navigate to the Patent Data Directory**:
   Change to the `patent_data` directory where the extraction scripts are located.

   ```bash
   cd patent_data
   ```
2. **Run the Extraction and Processing Scripts**:
  Execute the scripts sequentially to first download and then process the patent data from the USPTO.

  ```bash
  # Download patent data
  python patent_data_download.py

  # Process the downloaded raw patent text
  python patent_data_integration.py
```


### Data Preprocessing
#### Academic Data Preprocessing
**s2orc** dataset is sourced from Semantic Scholar and provided a comprehensive list of data fields for each academic paper. Below is the list of fields that we selected for this project:
1. **corpusid** : unique identifier for each paper
2. **title** : title of the research paper
3. **abstract** : abstract of the research paper
4. **s2FieldsOfStudy** : list of academic categories for each paper, using external or internal classifiers. The source can be the trained model or the original conference where the paper was submitted.

For the **abstract** and **title** fields standard preprocessing was applied which involved removing extra whitespaces, urls, numbers and special symbols.

#### Financial Data Preprocessing
The dataset is sourced from **Refinitive Workspace** and includes a comprehensive financial records of public and private companies. For the company details below is the list of fields that we selected for this project :

1. **Investee Company Name** - Name of the company (also the link to investments table)
2. **Investee Company Nation** - Nation the company is based out of
3. **Investee Company Founded Date\n('|')** - Date the company was officially founded eg. "1987-01-01 00:00:00"
4. **Investee Company TRBC Industry Group\n('|')** - TRBC is a market-based classification system. Organizations are assigned an industry on-the-basis of the market they serve rather than the products or services they offer. It has about 62  market categories.
5. **Investee Company Long Business Description\n('|')** - Long description detailing the work/product and other details of a company.
6. **Investee Company Short Business Description\n('|')** - Short description detailing the work/product and other details of a company.

For the investment round details below is the list of fields that we selected for this project:

1. **Investee Company Name** - Name of the company (also the link to companies table)
2. **Investment Date** - Date the investment was made
3. **Deal Rank Value\n(USD, Millions)** - Amount of Investment made in a round by all investors combined.

#### Patent Data Preprocessing
Patent dataset is sourced from USPTO and provided a comprehensive list of data fields for each granted paper. Below is the list of fields that we selected for this project:

1. **Publication and Application References:** Details of publication and initial application of the patents.
2. **Classification Details:** Categorization of patents according to international and national classification systems, like IPC and CPC.
3. **Inventor and Examiner Information:** Names and details of inventors, along with information about the USPTO examiners.
4. **Abstracts and Titles of Inventions:** Summary and official titles of the patented inventions.
5. **Citations:** References to prior patents or literature cited in the patent document.
6. **Applicant Data:** Information about the applicants, including organizations or individuals.
7. **Inventor Details:** Comprehensive details of the inventors including their names, addresses, and nationalities.
8. **Agent and Assignee Information:** Details about the patent agents and assignees, including names and addresses.

## Algorithm
### 1. Keyword/Topic/Phrase Identification
This step focuses on the automatic identification of keywords, topics, and phrases that serve as the core elements within research papers and company overviews. This critical step aims to extract and highlight the central themes and concepts present in textual documents. This process lays the groundwork for comprehensive data analysis and deeper insights into the relationships between financial data and research findings.

Below are the methods we are experimenting with for this step :  
1. **Noun Phrase Identification** : Unsupervised noun phrase identification using the Gensim and NLTK libraries. 
2. **BertTopic** : Using BertTopic package to identify topics using pretrained language models. A detailed detailed explanation of BertTopic is provided at [BertTopic](static/berttopic.md)

### 2. Cross Domain Topic Mapping
This step is designed to facilitate the mapping of keywords and topics extracted from academic research papers to the financial domain. By doing so, it empowers researchers and analysts to delve into the intricate relationships between funding flows and ongoing academic research. Through this mapping process, we aim to gain deeper insights into how financial factors intersect with and influence the world of academia.

We are experimenting with the below methods to create this mapping 
1. Word Embedding with Cosine Similarity
2. Word Embedding and Char-Based Features with Cosine Similarity
3. DBPedia Concept Normalization and Relationship Graph

### 3. Time Series Modelling
### 4. Data Trend and Visualization
**Basic Plotting** : 
This step is aimed at visualizing and analyzing trends in both research and financial data over a specified time frame, typically the last 20 years. This is a critical step for gaining insights into the data and understanding the growth patterns in both domains, as well as how they mutually influence each other.

#### Key Trends and Plots
We generate various trends and plots, including:

1. **Number of Unique Authors per Field**: This trend examines the number of unique authors in a particular field over the last 20 years, based on the first 30,000 papers.

2. **Number of Computer Science Publications**: This trend focuses on the number of publications in the field of Computer Science over the last 20 years.

3. **Number of Medicine Publications**: This trend tracks the number of publications in the field of Medicine over the last 20 years.

We utilize the Matplotlib and Plotly libraries to create interactive visualizations of these trends. Additionally, our plots include a moving average (rolling mean) with window sizes of 5 and 3 for the second and third plots, respectively. This smoothing technique helps to effectively visualize and understand any sudden fluctuations in the trends.

#### Dual Trend Analysis
Our analysis goes a step further by presenting a dual trend within a single graph. One trend represents research data, while the other represents financial data. This dual trend visualization enhances our understanding of the interplay and influence between these two domains.
By examining these trends, we gain valuable insights into the relationship between research and financial data over time, facilitating a more comprehensive understanding of their dynamics and impact on each other.


[Team](static/Teams.md)

[Updates](static/Updates.md)

[Tutorials/Examples](static/Tutorials.md)


