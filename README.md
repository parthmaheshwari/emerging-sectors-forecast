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

After conducting a thorough analysis of these datasets, taking into account factors such as feature richness and data update frequency, we have made the strategic decision to primarily utilize S2ORC for academic data, which comprises an extensive collection of research papers. Additionally, we have chosen to incorporate data from Refinitive Workspace to provide comprehensive coverage of the financial domain. The resources used to collect these two datasets are provided in the aforementioned Datasets table.

### Data Preprocessing
#### Academic Data Preprocessing
**s2orc** dataset is sourced from Semantic Scholar and provided a comprehensive list of data fields for each academic paper. Below is the list of fields that we selected for this project:
1. **corpusid** : unique identifier for each paper
2. **title** : title of the research paper
3. **abstract** : abstract of the research paper
4. **s2FieldsOfStudy** : list of academic categories for each paper, using external or internal classifiers. The source can be the trained model or the original conference where the paper was submitted.

For the **abstract** and **title** fields standard preprocessing was applied which involved removing extra whitespaces, urls, numbers and special symbols.

#### Financial Data Preprocessing
The dataset is sourced from **Refinitive Workspace** and includes a comprehensive financial records of public and private companies. For e.g. funding rounds, etc. Below is the list of fields that we selected for this project :
1. @parth will provide the details

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


