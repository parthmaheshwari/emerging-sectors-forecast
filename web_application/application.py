import time
import pandas as pd
import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import datetime
import os
#import config
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from pprint import pprint
from app_utils import CONCEPTID2CHILDIDS, CONCEPTID2NAME
from app_utils import CONCEPTNAME2ID, SUGGESTIONS_FOR_INPUT
from app_utils import depth_first_search_to_get_all_children_concepts
from app_utils import AZURE_FINANCE_SETTINGS, AZURE_ACADEMIC_SETTINGS, AZURE_PATENTS_SETTINGS
from app_utils import get_azure_finance_containers, get_azure_academic_containers, get_azure_patents_containers
from app_utils import get_finance_data, get_academic_data, get_patents_data, apply_min_max_scaling
from app_utils import create_plotly_graph_object

st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)


# Cosmos DB client
if 'client_finance' not in st.session_state:
    st.session_state.client_finance = cosmos_client.CosmosClient(
        AZURE_FINANCE_SETTINGS['host'], {'masterKey': AZURE_FINANCE_SETTINGS['master_key']},
        user_agent="CosmosDBPythonQuickstart",
        user_agent_overwrite=True
    )

# do the same for academic data
if 'client_academic' not in st.session_state:
    st.session_state.client_academic = cosmos_client.CosmosClient(
        AZURE_ACADEMIC_SETTINGS['host'], {'masterKey': AZURE_ACADEMIC_SETTINGS['master_key']},
        user_agent="CosmosDBPythonQuickstart",
        user_agent_overwrite=True
    )

# do the same for patents data

if 'client_patents' not in st.session_state:
    st.session_state.client_patents = cosmos_client.CosmosClient(
        AZURE_PATENTS_SETTINGS['host'], {'masterKey': AZURE_PATENTS_SETTINGS['master_key']},
        user_agent="CosmosDBPythonQuickstart",
        user_agent_overwrite=True
    )


# getting container for finance
if 'finance_db' not in st.session_state:
    st.session_state.finance_db, st.session_state.container_companies, st.session_state.container_investments = \
        get_azure_finance_containers(
            st.session_state.client_finance,
            AZURE_FINANCE_SETTINGS
        )


# getting container for finance
if 'academic_db' not in st.session_state:
    st.session_state.academic_db, st.session_state.container_academic = \
        get_azure_academic_containers(
            st.session_state.client_academic,
            AZURE_ACADEMIC_SETTINGS
        )

# getting container for finance
if 'patents_db' not in st.session_state:
    st.session_state.patents_db, st.session_state.container_patents = \
        get_azure_patents_containers(
            st.session_state.client_patents,
            AZURE_PATENTS_SETTINGS
        )


# Title and subtitle
st.write("""
# Analysing Funding Flows in Private Markets Using Academic Signals and Patent Data
#### This application is an in-depth exploration of the work we have done as a team.
- Select Interesting terms in Ontology
- Get all the children of these terms from the Ontology
- Generates queries according to the input
- Fetches data using the queries from the Azure CosmosDB
- Using the data generates plots.
"""
)

st.write("""
-----
""")

st.write("""
#### Please select some concepts for which you want to see the analysis.
""")

input_concept_names = st.multiselect(
    'Concepts to see analysis on',
    SUGGESTIONS_FOR_INPUT,
    ['Natural language understanding','Natural language generation'] #, 'Continuous modelling', 'Natural language processing', 'Social software']
)

text = st.text_area(
    "You Selected the below Concepts :",
    ', '.join(input_concept_names)

)

# expanding concepts
# Getting the required ids 
input_concept_ids = [CONCEPTNAME2ID[i] for i in input_concept_names]
# print('INPUT Concept Ids : {}'.format(input_concept_ids))
concept_ids_to_be_used_for_querying = depth_first_search_to_get_all_children_concepts(
    input_concept_id_list=input_concept_ids,
    conceptid2childids=CONCEPTID2CHILDIDS
)
# print('Expanded concepts : {}'.format(concept_ids_to_be_used_for_querying))
text2 = st.text_area(
    "Below are the {} expanded concepts".format(len(concept_ids_to_be_used_for_querying)),
    ', '.join([CONCEPTID2NAME[i] for i in concept_ids_to_be_used_for_querying])
)

st.write("""
-----
""")

# running queries
if 'finance_df' not in st.session_state:
    st.session_state.finance_df = pd.DataFrame()
    st.session_state.finance_df['year'] = [2001, 2002]
    st.session_state.finance_company_df = pd.DataFrame()
    st.session_state.finance_company_df['company name'] = ['ABC']

if 'academic_df' not in st.session_state:
    st.session_state.academic_df = pd.DataFrame()
    st.session_state.academic_df['year'] = [2001, 2002]

if 'patents_df' not in st.session_state:
    st.session_state.patents_df = pd.DataFrame()
    st.session_state.patents_df['year'] = [2006, 2007]



# Finance Data 
if st.button('Hit Finance COSMOS Database'):
    temp_time_start = time.time()
    with st.spinner('Please Wait while the database returns the output'):
        st.session_state.finance_df, st.session_state.finance_company_df = get_finance_data(
            concept_id_list=concept_ids_to_be_used_for_querying,
            container_companies=st.session_state.container_companies, 
            container_investments=st.session_state.container_investments
        ) 
    temp_time_end = time.time()
    st.write("Time taken to query Finance Data : {:.2f} Seconds".format(temp_time_end-temp_time_start))


    
    st.write(
        "Total Companies Found for the concepts : {}".format(
            st.session_state.finance_company_df["company name"].unique().shape[0]
        )
    )

if st.button('Show finance Company dataframe'):
    st.dataframe(
        st.session_state.finance_company_df[['company name','description','openalex concepts']],
        hide_index=True
    )

if st.button('Show finance dataframe'):
    st.dataframe(
        st.session_state.finance_df,
        column_config={
            "year": st.column_config.TextColumn(
                "year",
            ),
        },
        hide_index=True
    )


st.write("""
-----
""")
# Academic Data
if st.button('Hit Academic COSMOS Database'):
    temp_time_start = time.time()
    with st.spinner('Please Wait while the database returns the output'):
        st.session_state.academic_df = get_academic_data(
            concept_id_list=concept_ids_to_be_used_for_querying,
            container=st.session_state.container_academic
        ) 
    temp_time_end = time.time()
    st.write("Time taken to query Finance Data : {:.2f} Seconds".format(temp_time_end-temp_time_start))



if st.button('Show Academic dataframe'):
    st.dataframe(
        st.session_state.academic_df,
        column_config={
            "year": st.column_config.TextColumn(
                "year",
            ),
        },
        hide_index=True
    )

st.write("""
-----
""")

# Patents Data
if st.button('Hit Patents COSMOS Database'):
    temp_time_start = time.time()
    with st.spinner('Please Wait while the database returns the output'):
        st.session_state.patents_df,st.session_state.patents_df_with_concepts = get_patents_data(
            concept_id_list=concept_ids_to_be_used_for_querying,
            container=st.session_state.container_patents
        ) 
    temp_time_end = time.time()
    st.write("Time taken to query Patents Data : {:.2f} Seconds".format(temp_time_end-temp_time_start))

if st.button('Show Patents dataframe'):
    st.dataframe(
        st.session_state.patents_df,
        column_config={
            "year": st.column_config.TextColumn(
                "year",
            ),
        },
        hide_index=True
    )


if st.button('Glimpse of Patents With Concepts'):
    st.dataframe(
        st.session_state.patents_df_with_concepts,
        column_config={
            "year": st.column_config.TextColumn(
                "year",
            ),
        },
        hide_index=True
    )

st.write("""
-----
""")
smoothing_enabled = st.checkbox("Enable Smoothing")
enable_scaling = st.checkbox('Enable MinMax Scaling')
min_max_scaled=False

if enable_scaling:
    min_max_scaled=True
    scaled_finance_df = apply_min_max_scaling(st.session_state.finance_df, ['deal rank value(usd, millions)','company count'])
    scaled_academic_df = apply_min_max_scaling(st.session_state.academic_df, ['publication count','academic citations count', 'academic reference count', 'academic influential citations count'])
    scaled_patents_df = apply_min_max_scaling(st.session_state.patents_df, ['patents count', 'patent citations count'])
else:
    min_max_scaled=False
    scaled_finance_df = st.session_state.finance_df
    scaled_academic_df = st.session_state.academic_df
    scaled_patents_df = st.session_state.patents_df

if smoothing_enabled:
    scaled_finance_df = st.session_state.finance_df
    scaled_academic_df = st.session_state.academic_df
    scaled_patents_df = st.session_state.patents_df

    # Input for Window size
    window_size = st.number_input("Enter the value of k (window size):", min_value=1, step=1)

    if st.button("Apply Smoothing"):
        scaled_finance_df['deal rank value(usd, millions) smoothed'] = \
            scaled_finance_df['deal rank value(usd, millions)'].rolling(window=window_size).mean()
        scaled_finance_df['company count smoothed'] = \
            scaled_finance_df['company count'].rolling(window=window_size).mean()
        scaled_patents_df['patent citations count smoothed'] = \
            scaled_patents_df['patent citations count'].rolling(window=window_size).mean()
        scaled_patents_df['patents count smoothed'] = \
            scaled_patents_df['patents count'].rolling(window=window_size).mean()
        scaled_academic_df['publication count smoothed'] = \
            scaled_academic_df['publication count'].rolling(window=window_size).mean()
        scaled_academic_df['academic reference count smoothed'] = \
            scaled_academic_df['academic reference count'].rolling(window=window_size).mean()
        scaled_academic_df['academic citations count smoothed'] = \
            scaled_academic_df['academic citations count'].rolling(window=window_size).mean()
        scaled_academic_df['academic influential citations count smoothed'] = \
            scaled_academic_df['academic influential citations count'].rolling(window=window_size).mean()
        
    if enable_scaling:
        scaled_finance_df = apply_min_max_scaling(st.session_state.finance_df, ['deal rank value(usd, millions) smoothed','company count smoothed'])
        scaled_academic_df = apply_min_max_scaling(st.session_state.academic_df, ['publication count smoothed','academic citations count smoothed', 'academic reference count smoothed', 'academic influential citations count smoothed'])
        scaled_patents_df = apply_min_max_scaling(st.session_state.patents_df, ['patents count smoothed', 'patent citations count smoothed'])


    if st.button('Create Plots from Data'):
        f1 = create_plotly_graph_object(
            '', scaled_finance_df, scaled_academic_df, scaled_patents_df,
            'year', 'year','year', 'company count smoothed', 'publication count smoothed', 'patents count smoothed',min_max_scaled
        )
        f2 = create_plotly_graph_object(
            '', scaled_finance_df, scaled_academic_df, scaled_patents_df,
            'year', 'year','year', 'deal rank value(usd, millions) smoothed', 'academic citations count smoothed', 'patent citations count smoothed',min_max_scaled
        )

        f3 = create_plotly_graph_object(
            '', scaled_academic_df, scaled_academic_df, scaled_academic_df,
            'year', 'year','year', 'academic reference count smoothed', 'academic influential citations count smoothed', 'academic citations count smoothed',min_max_scaled
        )

        st.plotly_chart(f1, use_container_width=True)
        st.plotly_chart(f2, use_container_width=True)
        st.plotly_chart(f3, use_container_width=True)




else:

    if st.button('Create Plots from Data'):
        f1 = create_plotly_graph_object(
            '', scaled_finance_df, scaled_academic_df, scaled_patents_df,
            'year', 'year','year', 'company count', 'publication count', 'patents count',min_max_scaled
        )
        f2 = create_plotly_graph_object(
            '', scaled_finance_df, scaled_academic_df, scaled_patents_df,
            'year', 'year','year', 'deal rank value(usd, millions)', 'academic citations count', 'patent citations count',min_max_scaled
        )

        f3 = create_plotly_graph_object(
            '', scaled_academic_df, scaled_academic_df, scaled_academic_df,
            'year', 'year','year', 'academic reference count', 'academic influential citations count', 'academic citations count',min_max_scaled
        )

        st.plotly_chart(f1, use_container_width=True)
        st.plotly_chart(f2, use_container_width=True)
        st.plotly_chart(f3, use_container_width=True)


        
