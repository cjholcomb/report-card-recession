from urllib.request import urlopen
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("data/EDA_dataset.csv",
                   dtype={"area_fips": str})

df_2001 = df[(df['year'] == 2001)]
df_2008 = df[(df['year'] == 2008)]

# df['area_fips'] = df['area_fips'].astype(str)
# print(df['area_fips'][0])

import plotly.express as px

# fig, ax = plt.subplots()
# ax = plt.hist(df['delta'])
# plt.show()


fig = px.choropleth(df_2001, geojson = counties, locations='area_fips', color='delta_percap', 
                           color_continuous_scale="piyg",
                           color_continuous_midpoint=0,
                           range_color = (-0.25,0.25),
                           scope="usa",
                           labels={'delta':'Change in jobs'},
                           title= '2001: per capita'
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.suptitle('2001 Job Growth per capita')
fig.show()

fig = px.choropleth(df_2001, geojson = counties, locations='area_fips', color='delta', 
                           color_continuous_scale="Spectral",
                           color_continuous_midpoint=0,
                           scope="usa",
                           range_color=(-10000, 10000),
                           labels={'delta':'Change in jobs'},
                           title= '2001: Total delta'
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.suptitle('2001 Job')
fig.show()

fig = px.choropleth(df_2008, geojson = counties, locations='area_fips', color='delta_percap', 
                           color_continuous_scale="prgn",
                           color_continuous_midpoint=0,
                           range_color = (-0.25,0.25),
                           scope="usa",
                           labels={'delta':'Change in jobs'},
                           title= '2008: per capita'
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.suptitle('2008 Job Growth per capita')
fig.show()

fig = px.choropleth(df_2008, geojson = counties, locations='area_fips', color='delta', 
                           color_continuous_scale="rdylgn",
                           color_continuous_midpoint=0,
                           scope="usa",range_color=(-10000, 10000),
                           labels={'delta':'Change in jobs'},
                           title= '2008: Total delta'
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.suptitle('2008 Job Growth')
fig.show()

