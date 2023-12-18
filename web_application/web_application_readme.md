# Web Application Details

## Introduction
We created a simple user friendly web application based on Streamlit and Azure CosmosDB. The documents provides further detailed information about the application. We provide access to the hosted databases too. 


## Application and hosting
We are currently working on finding a suitable way to host the application as a full fledged website. Right now, we are just deploying a Streamlit application. The application can be accessed at : [WebApp]()

## Database 
We are using Azure CosmosDB database for the web application. Publications database (just computer science field of study) and companies and investment data (just for technology field) have been ported to Azure CosmosDB. We are currently in the process of porting patents data from USPTO. Below is the schema for the companies, investments and academic data. 

#### Companies Data Schema
#### Investments Data Schema
#### Academic Data Schema
#### Patents Data Schema
- Coming soon. 

In comning weeks, we will integrate the patents data into the web application too.


## Methodology
1. User selects one or multiple interesting concepts from the dropdown
2. Using depth first search we expand this list of concepts using the hierarchical ontology from [OpenAlex Ontology](https://docs.google.com/spreadsheets/d/1LBFHjPt4rj_9r0t0TTAlT68NwOtNH8Z21lBMsJDMoZg/edit#gid=575855905). 
3. Finance Data :
    - Using the expanded concepts list we fetch all the company names which have atleast one of these concepts tagged.
    - Using the company list from the previous step, we fetch all the investment from the Azure.
4. Academic Data :
    - Given the expanded list of concepts we fetch all the publications which have atleast one of these concepts tagged.
5. We create plots to see trends between investments and publications. 