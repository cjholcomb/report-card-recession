from urllib.request import urlopen
from src.dictionaries import *
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

'''This file is used to produce choropleth maps'''


def load_data():
    '''
    Produces three dataframes, one for each year.

    Params: none
    Returns: df_2001, df_2008, df_2020'''

    #loads the full training dataset
    df = pd.read_json("data/training_dataset.json",
                   dtype={"area_fips": str})

    #adds parent state and abbreviation to dataframe
    df['state_parent'] = df['area_fips'].map(state_lookup)
    df['state_abbr'] = df['state_parent'].map(state_abbr)
    
    #adds a column to differentiate map units
    df['area_type'] = np.nan
    for index, row in df.iterrows():
        if row['city']:
            df['area_type'][index] = 'city'
        elif row['state']:
            df['area_type'][index] = 'state'
        elif row['aggregated']:
            df['area_type'][index] = 'national'
        else:
            df['area_type'][index] = 'county'
    
    #adds a column scaling the job growth by the total number of jobs
    df['delta_scaled'] = df['delta'] /df['10']

    #drops the features to reduce size of dataframes
    df.drop(columns = features, inplace = True)


    #loads the prediction dataset, resetting the index
    df_2020 = pd.read_json('data/prediction_2020.json').reset_index().rename(columns = {'index':'area_fips'}) 
    df_2020['area_title'] = df_2020['area_fips'].map(area_dict) 
    
    #adds parent state and abbreviation to dataframe
    df_2020['state_parent'] = df_2020['area_fips'].map(state_lookup)
    df_2020['state_abbr'] = df_2020['state_parent'].map(state_abbr)
    
    #adds a column to differentiate map units
    df_2020['area_type'] = np.nan
    for index, row in df_2020.iterrows():
        if row['city']:
            df_2020['area_type'][index] = 'city'
        elif row['state']:
            df_2020['area_type'][index] = 'state'
        elif row['aggregated']:
            df_2020['area_type'][index] = 'national'
        else:
            df_2020['area_type'][index] = 'county'


    #drops the features to reduce size 
    df_2020.drop(columns = features, inplace = True)
    df_2020.drop(columns = extra_2020_columns, inplace = True)

    return df, df_2020

def map(year, division, df):
    if year == '2001':
        df = df[df['year'] == 2001]
        cmap = "PiYg"
        variable = 'delta_scaled'
        range_color = (-1,1)
        color_midpoint = 0
    elif year == '2008':
        df = df[df['year'] == 2008]
        cmap = "PRGn"
        variable = 'delta_scaled'
        range_color = (-1,1)
        color_midpoint = 0
    elif year == '2020':
        cmap = 'Spectral'
        variable = 'recov_likelihood'
        range_color = (0.25,1)
        color_midpoint = .5
    else:
        print('Invalid Year')
        pass
    
    if division == 'county':
            df = df[df.area_type == 'county']
            fig = px.choropleth(df, geojson = counties, locations='area_fips', color=variable, 
                            color_continuous_scale=cmap,
                            color_continuous_midpoint=color_midpoint,
                            range_color =  range_color,
                            scope="usa",
                            labels={'delta_scaled':'Job Growth', 'recov_likelihood':'Likelihood of Recovery'},
                            title= '2001 Job Growth'
                            )
            fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            fig.show()
    elif division == 'state':
            df = df[df.area_type == 'state']
            fig = px.choropleth(df, locationmode='USA-states', locations='state_abbr', color=variable, 
                            color_continuous_scale=cmap,
                            color_continuous_midpoint=color_midpoint,
                            range_color =  range_color,
                            scope="usa",
                            labels={'delta_scaled':'Job Growth', 'recov_likelihood':'Likelihood of Recovery'},
                            title= '2020 Forecast'
                            )
            fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'), margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
            fig.show()
    else:
        print('Invalid Division')
        pass

    
def map_2001():
    '''
    Creates a map of 2001 by county

    params: none
    returns: none
    loads map in web browser'''
    fig = px.choropleth(df_2001, geojson = counties, locations='area_fips', color='delta_scaled', 
                            color_continuous_scale="PiYg",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'job_growth':'Job Growth'},
                            title= '2001 Job Growth'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2008():
    '''
    Creates a map of 2008 by county

    params: none
    returns: none
    loads map in web browser'''
    fig = px.choropleth(df_2008, geojson = counties, locations='area_fips', color='delta_scaled', 
                            color_continuous_scale="PRGn",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'delta_scaled':'Job Growth'},
                            title= '2008 Job Growth'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2001_states():
    '''
    Creates a map of 2001 by state

    params: none
    returns: none
    loads map in web browser'''
    df_states = pd.read_csv('data/for_statemap.csv')
    fig = px.choropleth(df_states, locationmode='USA-states', locations='state', color='job_growth', 
                            color_continuous_scale="PiYg",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'job_growth':'Job Growth'},
                            title= '2001  Job Growth'
                            )
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'), margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2008_states():
    '''
    Creates a map of 2008 by state

    params: none
    returns: none
    loads map in web browser'''
    df_states = pd.read_csv('data/for_statemap.csv')
    fig = px.choropleth(df_states, locationmode='USA-states', locations='state', color='job_growth', 
                            color_continuous_scale="PRGn",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'job_growth':'Job Growth'},
                            title= '2008 Job Growth'
                            )
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'), margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2020():
    fig = px.choropleth(df_2020, geojson = counties, locations='area_fips', color='recov_likelihood', 
                            color_continuous_scale="Spectral",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'recov_likelihood':'Likelihood of Recovery'},
                            title= '2020 Recovery Probabilities: Counties'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2020_states():
    fig = px.choropleth(df_2020, geojson = counties, locations='area_fips', color='recov_likelihood', 
                            color_continuous_scale="Spectral",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'recov_likelihood':'Likelihood of Recovery'},
                            title= '2008 Job Growth'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

if __name__ == "__main__":
    df, df_2020 = load_data()

    
