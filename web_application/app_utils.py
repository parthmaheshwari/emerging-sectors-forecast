import datetime
import os
#import config
import random
import json
import pandas as pd
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from plotly.subplots import make_subplots
import plotly.graph_objs as go


# loading concepts used in academic for effecient query
ALL_ACADEMIC_CONCEPTS_IDS = set([i.strip() for i in open('../data/all_academic_concept_ids.txt').readlines()])

# loading concepts used in finance for effecient query
ALL_FINANCE_CONCEPTS_IDS = set([i.strip() for i in open('../data/all_finance_openalex_concept_ids.txt').readlines()])

# loading concepts used in patents for effecient query
ALL_PATENTS_CONCEPTS_IDS = set([i.strip() for i in open('../data/all_patent_concept_ids.txt').readlines()])


CONCEPTID2NAME = json.load(open('../data/openalex_concept_id_to_name_mapping.json', 'r'))
CONCEPTNAME2ID = {
    i: j
    for j, i in CONCEPTID2NAME.items()
}

CONCEPTID2CHILDIDS = json.load(open('../data/openalex_parent_to_children_mapping.json', 'r'))

SUGGESTIONS_FOR_INPUT = [i.strip() for i in list(CONCEPTNAME2ID.keys())] #[i.strip() for i in open('../data/all_good_suggestions.txt', 'r').readlines()]

AZURE_FINANCE_SETTINGS = json.load(open('../data/azure_api_details_finance.json', 'r'))
AZURE_ACADEMIC_SETTINGS = json.load(open('../data/azure_api_details_academic.json', 'r'))
AZURE_PATENTS_SETTINGS= json.load(open('../data/azure_api_details_patents.json', 'r'))


# Cosmos DB client
# CLIENT_FINANCE = cosmos_client.CosmosClient(
#     HOST, {'masterKey': AZURE_FINANCE_SETTINGS['master_key']},
#     user_agent="CosmosDBPythonQuickstart",
#     user_agent_overwrite=True
# )

def get_azure_finance_containers(client, settings):
    finance_db = client.get_database_client(settings['database_id'])
    container_companies = finance_db.get_container_client('companies')
    container_investments = finance_db.get_container_client('investments')
    return finance_db, container_companies, container_investments


def get_azure_academic_containers(client, settings):
    academic_db = client.get_database_client(settings['database_id'])
    container_academic = academic_db.get_container_client(settings['container_id'])
    return academic_db, container_academic

def get_azure_patents_containers(client, settings):
    patents_db = client.get_database_client(settings['database_id'])
    container_patents = patents_db.get_container_client(settings['container_id'])
    return patents_db, container_patents



def no_commas(number):
  return str(number).replace(",", "")


def depth_first_search_to_get_all_children_concepts(input_concept_id_list, conceptid2childids):
    '''
    DFS to get all the children of a concept
    '''
    visited = set()
    node_stack = input_concept_id_list
    all_children = set(input_concept_id_list)
    while node_stack:
        node = node_stack.pop()
        if node not in visited:
            node_children = conceptid2childids.get(node, [])
            all_children.update(set(node_children))
            node_stack += node_children
            
            visited.update([node])
    return list(all_children)


def get_finance_data(concept_id_list, container_companies, container_investments):

    # concept_id_list = list(set(concept_id_list).intersection(ALL_FINANCE_CONCEPTS_IDS))
    company_conditions = " OR ".join([f"ARRAY_CONTAINS(c.openalex_concept_ids, {int(concept_id)})" for concept_id in concept_id_list])
    company_query = f"""
        SELECT c.id as id,
        c.year as year,
        c.company_name AS "company name",
               c.investee_company_long_business_description as "description",
            c.openalex_concepts AS "openalex concepts"
        FROM companies c 
        WHERE {company_conditions}
        """

    company_items = list(container_companies.query_items(
        query=company_query,
        enable_cross_partition_query=True
    ))

    company_ids = [c['id'] for c in company_items]
    print('Total companies identified are : {}'.format(len(company_ids)))
    
    if len(company_items) > 0:

        investments_conditions =  ', '.join([f"'{id_}'" for id_ in company_ids])
        investment_query = f"""
        SELECT i.investment_year AS year, 
            i.deal_rank_value_usd_millions AS "deal rank value(usd, millions)", 
            i.investor_equity_total_usd_millions AS "investor equity total(usd, millions)", 
            i.disclosed_fund_equity_contribution_usd_millions AS "disclosed fund equity contribution(usd, millions)",
            i.round_equity_total_usd_millions AS "round equity total(usd, millions)",
            i.disclosed_debt_contribution_usd_millions AS "disclosed debt contribution(usd, millions)",
            i.deal_value_usd_millions AS "deal value(usd, millions)"
        FROM investments i
        WHERE i.company_id IN ({investments_conditions})
        """
        
        investment_items = list(container_investments.query_items(
            query=investment_query,
            enable_cross_partition_query=True
        ))
    else:
        company_items = [
            {
                'company name': '',
                'openalex concepts': '',
                'description': '',
            }
        ]
        investment_items = [
            {
                'year': 2021,
                'deal rank value(usd, millions)': 0,
                'investor equity total(usd, millions)': 0, 
                'disclosed fund equity contribution(usd, millions)': 0,
                'round equity total(usd, millions)': 0,
                'disclosed debt contribution(usd, millions)': 0,
                'deal value(usd, millions)': 0
            }
        ]
    print('Total investment datapoints fetched are : {}'.format(len(investment_items)))

    # company df
    df_company = pd.DataFrame.from_dict(company_items)
    company_count_by_year = df_company.groupby('year').size().reset_index(name='company count')
    print(df_company.head())
    
    #investment df
    df = pd.DataFrame.from_dict(investment_items)
    print(df.shape)
    if df.shape[0] > 0:
        df = df.groupby('year').sum().reset_index()
        df = df.merge(company_count_by_year, on='year', how='left')
        df['company count'] = df['company count'].fillna(0).astype(int)
    print(df.shape)
    print(df.head())

    return df, df_company


def get_academic_data(concept_id_list, container):

    concept_id_list = list(set(concept_id_list).intersection(ALL_ACADEMIC_CONCEPTS_IDS))
    academic_conditions = " OR ".join([f"ARRAY_CONTAINS(p.openalex_concept_ids, {int(concept_id)})" for concept_id in concept_id_list])

    academic_query = f"""
    SELECT p.year as year,
        p.referencecount as "academic reference count",
        p.citationcount as "academic citations count",
        p.influentialcitationcount as "academic influential citations count"
    FROM research_paper p
    WHERE (p.year >= 2000) AND ({academic_conditions}) 
    """

    academic_items = list(container.query_items(
        query=academic_query,
        enable_cross_partition_query=True
    ))
    print('Total academic data points are : {} '.format(len(academic_items)))
    
    df = pd.DataFrame.from_dict(academic_items)
    df['publication count'] = [1 for i in range(df.shape[0])]
    print(df.shape)
    if df.shape[0] > 0:
        df = df.groupby('year').sum().reset_index()
    
    print(df.shape)
    return df



def get_patents_data(concept_id_list, container):

    concept_id_list = list(set(concept_id_list).intersection(ALL_PATENTS_CONCEPTS_IDS))
    patents_conditions = " OR ".join([f"ARRAY_CONTAINS(p.openalex_concept_ids, {int(concept_id)})" for concept_id in concept_id_list])

    patents_query = f"""
    SELECT p.year as year,
    p.citation_count as "patent citations count"
    FROM tagged_patents_data p
    WHERE ({patents_conditions})
    """

    patents_items = list(container.query_items(
        query=patents_query,
        enable_cross_partition_query=True
    ))
    print('Total patents data points are : {} '.format(len(patents_items)))
    
    df = pd.DataFrame.from_dict(patents_items)
    df['patents count'] = [1 for i in range(df.shape[0])]
    print(df.shape)
    if df.shape[0] > 0:
        df = df.groupby('year').sum().reset_index()

    patents_query_with_concepts = f"""
    SELECT p["invention-title"] as title,
    p.abstract as abstract,
    p.openalex_concepts as "openalex concepts"
    FROM tagged_patents_data p
    WHERE ({patents_conditions})
    """
    patents_items_with_concepts = list(container.query_items(
        query=patents_query_with_concepts,
        enable_cross_partition_query=True
    ))
    df_with_concepts = pd.DataFrame.from_dict(patents_items_with_concepts).dropna()
    print(df.shape)
    return df,df_with_concepts

def apply_min_max_scaling(df, columns):
    scaler = MinMaxScaler()
    df_scaled = df.copy()
    df_scaled[columns] = scaler.fit_transform(df[columns])
    return df_scaled


def create_plotly_graph_object(
    sector, df1, df2, df3,
    df1_x_axis, df2_x_axis, df3_x_axis,
    df1_y_axis, df2_y_axis, df3_y_axis,min_max_scaled=False
):
    fig1 = go.Figure()


    # Add the line chart for patents count
    fig1.add_trace(
        go.Scatter(
            x=df3[df3_x_axis],
            y=df3[df3_y_axis],
            mode='lines+markers',
            name=df3_y_axis,
            yaxis='y3',  
            line=dict(color='blue'),
            # line=dict(shape='spline') 
        )
    )

    # Add the line chart for publication count
    fig1.add_trace(
        go.Scatter(
            x=df1[df1_x_axis],
            y=df1[df1_y_axis],
            mode='lines+markers',
            name=df1_y_axis,
            yaxis='y1',  # Set to the primary y-axis
            line=dict(color='red')
            # line=dict(shape='spline') 
        )
    )
    # Add the line chart for investment counts on the secondary y-axis
    fig1.add_trace(
        go.Scatter(
            x=df2[df2_x_axis],
            y=df2[df2_y_axis],
            mode='lines+markers',
            name=df2_y_axis,
            yaxis='y2',  # Set to the secondary y-axis,
            line=dict(color='green')
            # line=dict(shape='spline') 
        )
    )
    num_years_to_show = 10  # Change this as needed
    total_years = max(df1[df1_x_axis].max(), df2[df2_x_axis].max())
    min_year = min(df1[df1_x_axis].min(), df2[df2_x_axis].min())
    x_axis_tick_values = list(range(min_year, total_years + 1))
    
    # Customize the layout for fig1
    fig1.update_layout(
        title='Comparative Trend of {} Sector: {}, {}, and {} Over Years'.format(sector, df1_y_axis, df2_y_axis, df3_y_axis),
        xaxis_title='Year',
        xaxis=dict(
            tickvals=x_axis_tick_values,
            tickmode='array',
            tickangle=45  # Rotate x-axis labels for better readability
        ),

        yaxis=dict(title='{}'.format(df1_y_axis), side='left',titlefont=dict(color='red'), tickfont=dict(color='red'), showgrid=False),
        yaxis2=dict(title='{}'.format(df2_y_axis), side='right', overlaying='y',titlefont=dict(color='green'), tickfont=dict(color='green'), position=0.98, showgrid=False,showticklabels=not min_max_scaled),
        yaxis3=dict(title='{}'.format(df3_y_axis), side='right', overlaying='y',titlefont=dict(color='blue'), tickfont=dict(color='blue'), position=1, showgrid=False),
        legend=dict(
            x=1.1,  # Adjust the position of the legend to the side
            y=0.5,
            traceorder='normal',
            font=dict(family='Arial', size=10),
        ),
        height=400,  # Adjust the height as needed
        width=1600
    )
    return fig1

# investment_subset_df['Deal Value'] = investment_subset_df['Deal Value'].rolling(window=window_size).mean()
#             research_subset_df['Publications'] = research_subset_df['Publications'].rolling(window=window_size).mean()
#             research_subset_df['References'] = research_subset_df['References'].rolling(window=window_size).mean()
#             research_subset_df['Citations'] = research_subset_df['Citations'].rolling(window=window_size).mean()
