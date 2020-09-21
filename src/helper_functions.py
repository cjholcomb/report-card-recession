from src.dictionaries import *
import pandas as pd
import numpy as np 

def add_qtrid(df):
    '''
    adds a column for the year and quarter.

    params: df(dataframe)
    returns: dataframe with column added'''
    df['qtrid'] = df['year'] + (df['qtr']/4)
    return df

def import_one(year):
    '''brings a single year's woth of data into a dataframe. Used for initial EDA. 
    Referenced in import_all

    params: year(str)
    returns: df(dataframe)'''
    filepath = 'data/' + str(year) + '.csv'
    #all relevant csvs are renamed with only the year
    df = pd.read_csv(filepath, dtype = schema_dict)
    #schema_dict is found in dictionaries.py
    for column in drop_columns:
        if column in df.columns:
            df = df.drop([column], axis = 1)
    return df

def import_all(years):
    '''combines as many years ofdata into a single dataframe, as well as adding quater id
    References import_one and add_qtrid

    params: years (list of str)
    returns: df (dataframe)'''
    df = import_one(years[0])
    for year in years[1:]:
        df = df.append(import_one(year))
    df = add_qtrid(df)
    return df


def third_quarter(index):
    '''imports only every 3rd quarter row- required to import entire dataset (too large)
    Referenced in feature_space

    params: index, int
    returns: boolean'''
    if index == 0:
        return False
    elif (index - 3) % 4 == 0:
        return False
    else:
        return True

### Help functions for target calculation ###

def calc_nadir(s):
    assert isinstance(s, pd.Series)
    return s.min()

def calc_nadir_qtr(s):
    return s.argmin()

def calc_pre_peak(s):
    return s[ : s.argmin()].max()

def calc_pre_peak_quarter(s):
    try:
        qtr = s[ : s.argmin()].argmax()
    except:
        qtr = None
    return qtr

def calc_post_peak(s):
    return s[s.argmin() : ].max()

def calc_post_peak_qtr(s):
    return s[s.argmin() : ].argmax() + s.argmin()