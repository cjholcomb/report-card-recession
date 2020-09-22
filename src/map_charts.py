from urllib.request import urlopen
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_json("data/training_dataset.json",
                   dtype={"area_fips": str})

df['delta_scaled'] = df['delta'] /df['10']

df_2020 = pd.read_json('data/prediction_2020.json')


df_2001 = df[(df['year'] == 2001)]
df_2008 = df[(df['year'] == 2008)]



import plotly.express as px



def map_2001():
    fig = px.choropleth(df_2001, geojson = counties, locations='area_fips', color='delta_scaled', 
                            color_continuous_scale="Spectral",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'delta_scaled':'Job Growth'},
                            title= '2001 Job Growth'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2008():
    fig = px.choropleth(df_2008, geojson = counties, locations='area_fips', color='delta_scaled', 
                            color_continuous_scale="Spectral",
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
    df_states = pd.read_csv('data/for_statemap.csv')
    fig = px.choropleth(df_states, locationmode='USA-states', locations='state', color='job_growth', 
                            color_continuous_scale="Spectral",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'delta_scaled':'Job Growth'},
                            title= '2008 Job Growth'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

def map_2020():
    fig = px.choropleth(df_2020, geojson = counties, locations='area_fips', color='recov_likelihood', 
                            color_continuous_scale="rdylgn_r",
                            color_continuous_midpoint=0,
                            range_color = (-1,1),
                            scope="usa",
                            labels={'delta_scaled':'Job Growth'},
                            title= '2008 Job Growth'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    # fig.suptitle('2001 Job Growth per capita')
    fig.show()

# fig = px.choropleth(df_2001, geojson = counties, locations='area_fips', color='decline', 
#                            color_continuous_scale="prgn",
#                            range_color = (0,32),
#                            scope="usa",
#                            labels={'decline':'Quarters'},
#                            title= '2001 Quarters in Decline'
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # fig.suptitle('2001 Job Growth per capita')
# plt.show()

# fig = px.choropleth(df_2008, geojson = counties, locations='area_fips', color='decline', 
#                            color_continuous_scale="rdylgn_r",
#                            scope="usa",range_color=(0, 52),
#                            labels={'delta':'Change in jobs'},
#                            title= '2008: Total delta'
#                           )
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# # fig.suptitle('2008 Job Growth')
# fig.show()

