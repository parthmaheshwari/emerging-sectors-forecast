import datetime
import os
import config
import random
import json
import pandas as pd
import azure.cosmos.documents as documents
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objs as go


# loading concepts used in academic for effecient query
ALL_ACADEMIC_CONCEPTS_IDS = set([i.strip() for i in open('../data/all_academic_concept_ids.txt').readlines()])

# loading concepts used in finance for effecient query
ALL_FINANCE_CONCEPTS_IDS = set([i.strip() for i in open('../data/all_finance_openalex_concept_ids.txt').readlines()])


CONCEPTID2NAME = json.load(open('../data/openalex_concept_id_to_name_mapping.json', 'r'))
CONCEPTNAME2ID = {
    i: j
    for j, i in CONCEPTID2NAME.items()
}

CONCEPTID2CHILDIDS = json.load(open('../data/openalex_parent_to_children_mapping.json', 'r'))

SUGGESTIONS_FOR_INPUT = [i.strip() for i in open('../data/all_good_suggestions.txt', 'r').readlines()]

AZURE_FINANCE_SETTINGS = json.load(open('../data/azure_api_details_finance.json', 'r'))
AZURE_ACADEMIC_SETTINGS = json.load(open('../data/azure_api_details_academic.json', 'r'))



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

    concept_id_list = list(set(concept_id_list).intersection(ALL_FINANCE_CONCEPTS_IDS))

    company_conditions = " OR ".join([f"ARRAY_CONTAINS(c.openalex_concept_ids, {int(concept_id)})" for concept_id in concept_id_list])
    company_query = f"""
        SELECT c.id as id,
            c.company_name AS company_name,
            c.openalex_concepts AS openalex_concepts
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
            i.deal_rank_value_usd_millions AS deal_rank_value_usd_millions, 
            i.investor_equity_total_usd_millions AS investor_equity_total_usd_millions, 
            i.disclosed_fund_equity_contribution_usd_millions AS disclosed_fund_equity_contribution_usd_millions,
            i.round_equity_total_usd_millions AS round_equity_total_usd_millions,
            i.disclosed_debt_contribution_usd_millions AS disclosed_debt_contribution_usd_millions,
            i.deal_value_usd_millions AS deal_value_usd_millions
        FROM investments i
        WHERE i.company_id IN ({investments_conditions})
        """
        
        investment_items = list(container_investments.query_items(
            query=investment_query,
            enable_cross_partition_query=True
        ))
    else:
        investment_items = [
            {
                'year': 2021,
                'deal_rank_value_usd_millions': 0,
                'investor_equity_total_usd_millions': 0, 
                'disclosed_fund_equity_contribution_usd_millions': 0,
                'round_equity_total_usd_millions': 0,
                'disclosed_debt_contribution_usd_millions': 0,
                'deal_value_usd_millions': 0
            }
        ]
    print('Total investment datapoints fetched are : {}'.format(len(investment_items)))
    df = pd.DataFrame.from_dict(investment_items)
    print(df.shape)
    if df.shape[0] > 0:
        df = df.groupby('year').sum().reset_index()
    print(df.shape)
    print(df.head())

    # company df
    df_company = pd.DataFrame.from_dict(company_items)
    print(df_company.head())
    return df, df_company


def get_academic_data(concept_id_list, container):

    concept_id_list = list(set(concept_id_list).intersection(ALL_ACADEMIC_CONCEPTS_IDS))
    academic_conditions = " OR ".join([f"ARRAY_CONTAINS(p.openalex_concept_ids, {int(concept_id)})" for concept_id in concept_id_list])

    academic_query = f"""
    SELECT p.year as year,
        p.referencecount as referencecount,
        p.citationcount as citationcount,
        p.influentialcitationcount as influentialcitationcount
    FROM research_paper p
    WHERE (p.year >= 2000) AND ({academic_conditions}) 
    """

    academic_items = list(container.query_items(
        query=academic_query,
        enable_cross_partition_query=True
    ))
    print('Total academic data points are : {} '.format(len(academic_items)))
    
    df = pd.DataFrame.from_dict(academic_items)
    df['publicationcount'] = [1 for i in range(df.shape[0])]
    print(df.shape)
    if df.shape[0] > 0:
        df = df.groupby('year').sum().reset_index()
    
    print(df.shape)
    return df


def create_plotly_graph_object(
    sector, df1, df2,
    df1_x_axis, df2_x_axis,
    df1_y_axis, df2_y_axis,
):
    fig1 = go.Figure()

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
        title='Dual Trend of {} Sector: {} with {} Over Years'.format(sector, df1_y_axis, df2_y_axis),
        xaxis_title='Year',
        xaxis=dict(
            tickvals=x_axis_tick_values,
            tickmode='array',
            tickangle=45  # Rotate x-axis labels for better readability
        ),
        yaxis=dict(title='{} (USD, Millions)'.format(df1_y_axis), side='left', showgrid=False),
        yaxis2=dict(title='{} Counts'.format(df2_y_axis), side='right', overlaying='y', showgrid=False),
        legend=dict(
            x=1.1,  # Adjust the position of the legend to the side
            y=0.5,
            traceorder='normal',
            font=dict(family='Arial', size=12),
        ),
        height=400,  # Adjust the height as needed
    )
    return fig1

# investment_subset_df['Deal Value'] = investment_subset_df['Deal Value'].rolling(window=window_size).mean()
#             research_subset_df['Publications'] = research_subset_df['Publications'].rolling(window=window_size).mean()
#             research_subset_df['References'] = research_subset_df['References'].rolling(window=window_size).mean()
#             research_subset_df['Citations'] = research_subset_df['Citations'].rolling(window=window_size).mean()
