# Recession Report Card

## Purpose

The U.S. in the 21st century is not particularly adept at recovering from reccesions, and another one is upon us. This recession is likely to be deeper and longer than the last. Traditional measures of economic health (unemployment, GDP, stock market) are all too aggregated to be of much use for most Americans. Overall rise and/or fall does nothing for the outlook of a particular town or city. With this project I intend to break down economic data from the Bureau of Labor Statistics, and use the data to model and predict economic recovery. Specifically, I intend to answer:

1. Which areas (counties, states, cities) are likliest to recover from this recession, before the *next* recession.
2. How long will each area be in decline, before it begins to recover?
3. Once an area begins to recover, how long will it take?

## Previous Research

Most data science being applied to this type of problem are attempting to predict *when* a recession might occur (https://towardsdatascience.com/recession-prediction-using-machine-learning-de6eee16ca94,https://economics.rabobank.com/publications/2019/january/united-states-the-recession-of-2020/), but they often rely on indices of long-term economic performance. They also do not differentiate performance in different *sectors* of the economy, so the definition of a recovery can mean little to workers employed in sectors that falter. Some attempts to use sampled data have been successful (http://www.sundsoy.com/publications/tow.pdf), but would not provide the granularity I am looking for to narrow down recovery in specific areas.

## Definitions and Assumptions

### Recession Events

Each recession in my training data set (2001, 2008) have a particular *event* which corresponds with a sudden drop in economic forecasts (9/11 and the stock market crash of 2008). While these events are not necessaily the beginnings of their corresponding reccesions,they do represent the largest, steepest drops in employment. For the purposes of this project, the recession will be defined as beginning at these events.

### Pre-Recession Peak

This is defined as the 'high point' of employment numbers *before* the recession event.

### Nadir

This is defined as the point at which an areas job numbers reach their lowest point during the time period in question. 

### Recovery Point

When an area achieves its job numbers equal or greater than its Pre-Recession Peak before the next recession.

### Recovery (boolean)

Whether or not an area achieves a recovery point before the next recession.

### Post-Recession Peak

The 'high point' of jobs numbers *after* the nadir, but before the next recession event.

### Decline Time

The number of quarters between the Pre-Recession Peak and the Nadir.

### Recovery Time

The number of quarters between the Nadir and the Recovery Point

## New Approach

As stated above, economic data that is aggregated to the country or state level is too abstract to be of any use to workers or local leaders. I intend to make a more granular model that can be applied to individual political units (counties, cities, territories) to give a realistic forecast for each of them. Additionally, my dataset will use many more features, very specific breakdowns of industries in every area in question.

## Deliverables

In additon to creating a model and predictions for the entire US, I intend to make an interactive map, as well as a Flask webapp that will allow the end user to look up a particular area.

### Stretch Goals

Repeat the model on *wage* data rather than pure employment numbers.
Extend the model to predict Decline Time and Recovery Time as targets.
Extend the dataset to work on months rather than quarters.

## Dataset

I will be using the Bureau of Labor Statstics Quarterly Census of Employment and Wages. It contains about 4,700 records (double that for both recessions) as well as ~2,400 specific industries. I will aslo attempt to augment with a feature of my own (population_ from the U.S. Census bureau. Data is only available in (quite massive) csv files for download, but once they have been downloaded and consolidated I will be working with json files (models will be pickled).

## Potential Challenges

First challenge that comes to mind is calculating the decline and recovery time targets. I've had difficulty with that in the past. 
Second- population data. It might be difficult to wrangle the population data for the indivudal cities (I've already got them for the counties).
Third- Neural Networks. I've not had much success with these in the past. Some additional studying and practicing will need to be done.

## Short-term (weekend) plans:

### Saturday:

Complete Dataset, attempt to crack the decline/recovery time problem.
Bring out old models from capstone 2, set them on some really big gridsearches to get them tuned as well as possible in advance.

### Sunday:

Build a shell Flask app (doesn't do much other than display data from a json and a pickle file)
Produce CSS for flask app.
Develop some rudimentary NN models.
Save, chart, and pickle optimal models tuned last night.
