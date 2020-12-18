from dictionaries import *
from helper_functions import *
import pandas as pd
import numpy as np

#This file takes the quarterly raw data from the QCEW and turns them into quarterly timelines. From here, we can compute target variables.


def create_timeline_2001(variable):
    '''produces a dataframe of the 2001 recession timeline.
    
    Used to compute targets

    params: variable, str, one of ['month3_emplvel' (employment), 'avg_wkly_wage' (wages)]
    returns: df, Dataframe
    exports a json file (used in plotting results)
    '''
    
    #create a dataframe of the years in question
    df = import_all(recession1_years)

    #drop 'unknown or undefined' areas
    df = df[~df['area_fips'].str.contains("999")]
    
    #pivots the table to arrange quarters in columns, drops extraneous variables.
    df = df.pivot_table(columns = 'qtrid', values = variable, index = ['area_fips', 'area_title'], aggfunc = np.sum)
    df = df.reset_index()
    
    #fill nans
    df = df.fillna(0)

    #creates a secondary dataframe with only timeline variables
    df2 = df.drop(columns = ['area_fips', 'area_title'])
    df2 = df2.reset_index()
    
    #drops the index so that all calculations are free of any type mismatches
    df2 = df2.drop(columns = 'index')
    df2 = df2.fillna(0)


### DEPRECIATED CODE #### 

#     #this specifies when the jobs numbers "bottom-out" during the recession
#     nadir = df2.iloc[:,6:].apply(lambda x: calc_nadir(x), axis=1).rename('nadir')
    
#     #counts the number of quarters to the nadir since the beginning of the timeframe
#     nadir_qtr = df2.iloc[:,6:].apply(lambda x: calc_nadir_qtr(x), axis=1).rename('nadir_qtr')
    
#     #computes the highest points before and after the nadir, and captures the quarter count
#     pre_peak = df2.apply(lambda x: calc_pre_peak(x), axis=1).rename('pre_peak')
#     pre_peak_qtr = df2.apply(lambda x: calc_pre_peak_quarter(x), axis=1).rename('pre_peak_qtr')
#     post_peak = df2.apply(lambda x: calc_post_peak(x), axis=1).rename('post_peak')
#     post_peak_qtr = df2.apply(lambda x: calc_post_peak_qtr(x), axis=1).rename('post_peak_qtr')

### DEPRECIATED CODE #### 
    
    #specifies the lowest job numbers during the recession. Disregards quarters before the recession event. 
    df2['nadir'] = df2.iloc[:,6:].min(axis=1)

    #specifies which quarter the nadir occured.
    df2['nadir_qtr'] = df2.iloc[:,6:].idxmin(axis=1).apply(lambda x: df.columns.get_loc(x))
    
    #creates a column to store indices for lookup.
    df2['new'] = [df2.iloc[i].values for i in df.index]
    
    #specifies the highest job numbers *before* the nadir.
    df2['pre_peak'] = df2.apply(lambda x: max(x['new'][0:x['nadir_qtr']]), axis=1)
    
    #specifies the highest job numbers *after* the nadir
    df2['post_peak'] = df2.apply(lambda x: max(x['new'][x['nadir_qtr']:]), axis=1)
    
    #specifies which quarter the pre-peak occurred.
    df2['pre_peak_qtr'] = pd.Series([s[i] for i, s in zip(df2.index, df2['pre_peak'].apply(
        lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                   .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x))
    
    #specifies which quarter the post-peak occurred.
    df2['post_peak_qtr'] = pd.Series([s[i] for i, s in zip(df2.index, df2['post_peak'].apply(
        lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                   .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x))

    #PRIMARY TARGET: did the area decline the entire time(-1), did it start growing again but not avhieve it's former numbers(0), or did it grow and recover(1)?
    df2['recovery'] = (df2['post_peak'] >= df2['pre_peak']) *1
    
    #create another dataframe to calculate the # of quarters to recover- only contains recovered datapoints
    df3 = df2[df2['recovery'] == 1]
    
    #creates a column to derive the recovery quarter- list of boolean values
    df3['recovery_list'] = df3.apply(lambda x: (x['new'][x['nadir_qtr']:] >= x['pre_peak']), axis=1)

    #creates a column for the number or quarters until the results pass the pre-peak high, since the nadir
    df3['recovery_qtr'] = df3['recovery_list'].apply(lambda x: list(x).index(True))

    #creates a new dataset to store derived fields
    df_new = df2[['nadir', 'nadir_qtr', 'pre_peak', 'pre_peak_qtr', 'post_peak', 'post_peak_qtr', 'recovery']]
    
    #adds the recovery quarter column
    df_new = df_new.join(df3, join = left, rsuffix = '_recov')

    #puts the computed points in a dataframe, joins with timeline
    df = df.join(df_new, how = 'outer', rsuffix = '_derive')
    


    

    #SECONDARY TARGET: How long did the jobs numbers decline?
    df['decline'] = (df['nadir_qtr'] - df['pre_peak_qtr'])
    
    #TERTIARY TARGET: different in before/after jobs numbers
    df['delta'] = df['post_peak'] - df['pre_peak']
    
    #export the data
    df.to_json('data/Recession1_timeline.json')
    return df

def create_timeline_2008(variable):
    '''produces a dataframe of the 2008 recession timeline. Used to compute targets

    params: variable, str, one of ['month3_emplvel' (employment), 'avg_wkly_wage' (wages)]
    returns: df, Dataframe
    exports a json file (used in plotting results)
    '''
    
    #create a dataframe of the years in question
    df = import_all(recession2_years)

    #drop 'unknown or undefined' areas
    df = df[~df['area_fips'].str.contains("999")]
    
    #pivots the table to arrange quarters in columns, drops extraneous variables.
    df = df.pivot_table(columns = 'qtrid', values = variable, index = ['area_fips', 'area_title'], aggfunc = np.sum)
    df = df.reset_index()
    
    #fill nans
    df = df.fillna(0)

    #creates a secondary dataframe with only timeline variables
    df2 = df.drop(columns = ['area_fips', 'area_title'])
    df2 = df2.reset_index()
    
    #drops the index so that all calculations are free of any type mismatches
    df2 = df2.drop(columns = 'index')
    df2 = df2.fillna(0)


### DEPRECIATED CODE #### 

#     #this specifies when the jobs numbers "bottom-out" during the recession
#     nadir = df2.iloc[:,6:].apply(lambda x: calc_nadir(x), axis=1).rename('nadir')
    
#     #counts the number of quarters to the nadir since the beginning of the timeframe
#     nadir_qtr = df2.iloc[:,6:].apply(lambda x: calc_nadir_qtr(x), axis=1).rename('nadir_qtr')
    
#     #computes the highest points before and after the nadir, and captures the quarter count
#     pre_peak = df2.apply(lambda x: calc_pre_peak(x), axis=1).rename('pre_peak')
#     pre_peak_qtr = df2.apply(lambda x: calc_pre_peak_quarter(x), axis=1).rename('pre_peak_qtr')
#     post_peak = df2.apply(lambda x: calc_post_peak(x), axis=1).rename('post_peak')
#     post_peak_qtr = df2.apply(lambda x: calc_post_peak_qtr(x), axis=1).rename('post_peak_qtr')

### DEPRECIATED CODE #### 
    
    #specifies the lowest job numbers during the recession. Disregards quarters before the recession event. 
    df2['nadir'] = df2.iloc[:,6:].min(axis=1)

    #specifies which quarter the nadir occured.
    df2['nadir_qtr'] = df2.iloc[:,6:].idxmin(axis=1).apply(lambda x: df.columns.get_loc(x))
    
    #creates a column to store indices for lookup.
    df2['new'] = [df2.iloc[i].values for i in df.index]
    
    #specifies the highest job numbers *before* the nadir.
    df2['pre_peak'] = df2.apply(lambda x: max(x['new'][0:x['nadir_qtr']]), axis=1)
    
    #specifies the highest job numbers *after* the nadir
    df2['post_peak'] = df2.apply(lambda x: max(x['new'][x['nadir_qtr']:]), axis=1)
    
    #specifies which quarter the pre-peak occurred.
    df2['pre_peak_qtr'] = pd.Series([s[i] for i, s in zip(df2.index, df2['pre_peak'].apply(
        lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                   .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x))
    
    #specifies which quarter the post-peak occurred.
    df2['post_peak_qtr'] = pd.Series([s[i] for i, s in zip(df2.index, df2['post_peak'].apply(
        lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                   .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x))
    
    #creates a new dataset to store derived fields
    df_new = df2[['nadir', 'nadir_qtr', 'pre_peak', 'pre_peak_qtr', 'post_peak', 'post_peak_qtr']]
    
    #puts the computed points in a dataframe, joins with timeline
    df = df.join(df_new, how = 'outer', rsuffix = '_derive')
    
    #PRIMARY TARGET: did the area decline the entire time(-1), did it start growing again but not avhieve it's former numbers(0), or did it grow and recover(1)?
    df['recovery'] = (df['post_peak'] >= df['pre_peak']) *1

    #SECONDARY TARGET: How long did the jobs numbers decline?
    df['decline'] = (df['nadir_qtr'] - df['pre_peak_qtr'])
    
    #TERTIARY TARGET: different in before/after jobs numbers
    df['delta'] = df['post_peak'] - df['pre_peak']
    
    #export the data
    df.to_json('data/Recession2_timeline.json')
    return df

#produces the full feature set
def feature_space(year):
    '''
    params: year, int, one of [2001, 2008, 2020]
    
    returns: dataframe, 
    export a json file'''
    
    #import the dataset
    filepath = 'too_big_for_git/industry_' + str(year) + '.csv'
    if year != '2020':
        df = pd.read_csv(filepath, skiprows = lambda x: third_quarter(x), low_memory = False, usecols = [0,1,2,3,4,5,6,7,8,11,12,15])
    else:
        df = pd.read_csv(filepath,  low_memory = False,)

    #drop redundancy rows:
    df = df[df.own_code != 8]
    df = df[df.own_code != 9]
    
    #pivots the data, making industry code into columns
    df = df.pivot_table(columns = 'industry_code', values = 'month3_emplvl', index = ['area_fips'], aggfunc = np.max)
    
    #transforms the jobs numbers to proportions
    for column in df:
        if column == '10':
            continue
        else:
            df[column] = df[column] / df['10']
    
    #adds dummy variables for cities, states, and aggregated areas
    df = df.reset_index()
    df['city'] = df['area_fips'].str.contains('C') * 1
    df['state'] = df['area_fips'].apply(lambda x: 1 if x in state_abbr.keys() else 0)
    df['aggregated'] = df['area_fips'].str.contains('US') * 1
    
    #fill nans
    df = df.fillna(0)
    
    #adds area title to 2020 data
    if year == '2020':
        df['area_title'] = df['area_fips'].map(area_dict) 

    #reset the index to area_fips, the lookup variable
    df = df.set_index('area_fips')
    
    #exports the file as backup
    filepath = 'data/features_' + str(year) + '.json'
    
    #adds columns left off either year
    for column in missing_columns:
        if column not in df.columns:
            df[column] = 0
    

    
    #exports to json
    df.to_json(filepath)
    return df

def create_training_dataset():
    
    #create feature sets for 2001 and 2008
    df_2001_feat = feature_space('2001')
    df_2008_feat = feature_space('2008')
 
    #create timelines
    df_2001_timeline = create_timeline_2001('month3_emplvl')
    df_2001_timeline = df_2001_timeline.set_index('area_fips')
    df_2008_timeline = create_timeline_2008('month3_emplvl')
    df_2008_timeline = df_2008_timeline.set_index('area_fips')
    
    #join 2001 and drop timeline columns
    df_2001 = df_2001_feat.join(df_2001_timeline, how = 'left', rsuffix = 'dupe')
    df_2001 = df_2001.drop(columns=[ 2000.25, 2000.5, 2000.75, 2001.0, 2001.25, 2001.5, 2001.75, 2002.0, 2002.25, 2002.5, 2002.75, 2003.0, 2003.25, 2003.5, 2003.75, 2004.0, 2004.25, 2004.5, 2004.75, 2005.0, 2005.25, 2005.5, 2005.75, 2006.0, 2006.25, 2006.5, 2006.75, 2007.0, 2007.25, 2007.5, 2007.75, 2008.0, 'nadir', 'nadir_qtr',
        'pre_peak', 'pre_peak_qtr', 'post_peak_qtr', 'post_peak'])
    
    #adds a year variabble (not used in model)
    df_2001['year'] = '2001'
    df_2001 = df_2001.reset_index()
    
    #join 2008 and drop timeline columns
    df_2008 = df_2008_feat.join(df_2008_timeline, how = 'left', rsuffix = 'dupe')
    df_2008 = df_2008.drop(columns=[2007.25, 2007.5, 2007.75, 2008.0,
       2008.25, 2008.5, 2008.75, 2009.0, 2009.25, 2009.5, 2009.75, 2010.0, 2010.25, 2010.5, 2010.75, 2011.0, 2011.25, 2011.5, 2011.75,2012.0, 2012.25, 2012.5, 2012.75, 2013.0, 2013.25, 2013.5, 2013.75, 2014.0, 2014.25, 2014.5, 2014.75, 2015.0, 2015.25, 2015.5,
       2015.75, 2016.0, 2016.25, 2016.5, 2016.75, 2017.0, 2017.25, 2017.5, 2017.75, 2018.0, 2018.25, 2018.5, 2018.75, 2019.0, 2019.25, 2019.5, 2019.75, 2020.0, 'nadir', 'nadir_qtr',
        'pre_peak', 'pre_peak_qtr', 'post_peak_qtr', 'post_peak'])
    
    #adds a year variabble (not used in model)
    df_2008['year'] = '2008'
    df_2008 = df_2008.reset_index()
    
    #appends all rows into a single dataframe
    df_all = df_2001.append(df_2008)
    
    #export the data
    filepath = 'data/training_dataset.json'
    df_all = df_all[df_all['10'] != 0]
    
    #drop 'unknown or undefined' areas
    df_all = df_all.dropna()
    df_all = df_all.reset_index()
    df_all.to_json(filepath)
    
    #return all three datasets
    return df_all, df_2001, df_2008


if __name__ == '__main__':
    df_train, df_2001, df_2008 = create_training_dataset()
    df_predict = feature_space('2020')


 