import plotly.express as px
from urllib.request import urlopen
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response: counties = json.load(response)

df = pd.read_csv("data/2020_predict_results.csv",
                   dtype={"area_fips": str})

fig = px.choropleth(df, geojson = counties, locations='area_fips', color='likelihood1', 
                            color_continuous_scale= 'RdYlGn',
                           range_color = (0.3,0.7),
                           scope="usa",
                           labels={'delta':'Change in jobs'},
                           title= '2001: per capita'
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.suptitle('2001 Job Growth per capita')
fig.show()                   