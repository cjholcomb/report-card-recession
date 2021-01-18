import pandas as pd
import numpy as np
import cpi

from src.constants import *
from src.classes import *
# from recessions import Recession
# from industries import industry_titles

#schema for importing dataframe
schema_dict = { 'area_fips':str,  'own_code':str,  'industry_code':str,  'agglvl_code':str,  'size_code':str,  'year':int,  'qtr':int,  'disclosure_code':str, 'area_title':str,  'own_title':str,  'industry_title':str,  'agglvl_title':str,  'size_title':str,  'qtrly_estabs':int,  'month1_emplvl':int,  'month2_emplvl':int,  'month3_emplvl':int,  'total_qtrly_wages':int,  'taxable_qtrly_wages':int,  'qtrly_contributions':int,  'avg_wkly_wage':int,  'lq_disclosure_code':str,  'lq_qtrly_estabs':float,  'lq_month1_emplvl':float,  'lq_month1_emplv2':float,  'lq_month1_emplv3':float,  'lq_total_qtrly_wages':float,  'lq_taxable_qtrly_wages':float,  'lq_qrtly_contributions':float,  'oty_disclosure_code':str,  'oty_qtrly_estabs':int,  'oty_qtrly_estabs_pct_chg':float,  'oty_month1_emplvl_chg':int,  'oty_month1_emplvl_pct_chg':float,  'oty_month2_emplv_chg':int,  'oty_month2_emplvl_pct_chg':float,  'oty_month3_emplvl_chg':int,  'oty_month3_emplvl_pct_chg':float,  'oty_total_qtrly_wages_chg':int,  'oty_total_qtrly_wages_pct_chg':float,  'oty_taxable_qtrly_wages_chg':int,  'oty_taxable_qtrly_wages_pct_chg':float,  'oty_qrtly_contributions_chg':int,  'oty_qrtly_contributions_pct_chg':float,  'oty_avg_wkly_wage_chg':int,  'oty_avg_wkly_wage_pct_chg':float} 

#unused columns from QCEW
import_drop = ['own_code',  'size_code',  'disclosure_code',  'own_title',  'size_title',  'lq_disclosure_code', 'oty_disclosure_code',  'oty_month1_emplvl_chg',  'oty_month2_emplvl_chg',  'oty_month3_emplvl_chg',  'oty_total_qtrly_wages_chg',  'oty_taxable_qtrly_wages_chg',  'oty_qtrly_contributions_chg',  'oty_avg_wkly_wage_chg',  'lq_qtrly_estabs_count',  'lq_month1_emplvl',  'lq_month2_emplvl',  'lq_month3_emplvl',  'lq_total_qtrly_wages',  'lq_taxable_qtrly_wages',  'lq_qtrly_contributions',  'oty_qtrly_estabs_count_chg',  'oty_qtrly_estabs_count_pct_chg',  'oty_month1_emplvl_pct',  'oty_month2_emplvl_pct',  'oty_month3_emplvl_pct',  'oty_total_qtrly_wages_pct',  'oty_taxable_qtrly_wages_chg',  'oty_qtrly_contributions_pct',  'oty_avg_wkly_wage_pct',  'oty_taxable_qtrly_wages_chg.1',  'lq_avg_wkly_wage',  'taxable_qtrly_wages',  'qtrly_contributions']

def add_qtrid(df):
    '''
    Adds a column for the year and quarter. Needed for indexing.

        Parameters: 
            df (pandas dataframe)

        Returns:
            df (pandas dataframe): dataframe with column added
    '''
    df['qtrid'] = df['year'] + (df['qtr']/4)
    return df

def import_one(year, dimension = 'area'):
    '''
    Constructs a dataframe from a single year's worth of data.
    
        Parameters: 
            year (str): year of data to be imported
            dimension (str): dimension of data to import. Must be 'area' or 'industry'. Default = 'area'
        
        Returns:
            df (pandas dataframe)
    '''
    filepath = 'data/' + dimension + '_files/' + str(year) + '.csv'
    #all relevant CSVs should be named with only the year
    df = pd.read_csv(filepath, dtype = schema_dict)
    #removes redundant entries in industry files
    if dimension == 'industry':
        df = df[df.own_code != 8]
        df = df[df.own_code != 9]
    for column in import_drop:
        if column in df.columns:
            df = df.drop([column], axis = 1)
    #removes industry columns from area data
    if dimension == 'area':
        df = df.drop(columns = ['industry_code', 'industry_title'])
    #removes area columns from industry data
    elif dimension == 'industry':
        df = df.drop(columns = ['area_fips', 'area_title'])
    return df

def import_all(years, dimension = 'area'):
    '''
    Combines years of data into a single dataframe, adds qtrid

        Parameters: 
            years (list)
            dimension (str): dimension of data to import. Must be 'area' or 'industry'. Default = 'area'

        Returns: 
            df (dataframe)
    '''
    df = import_one(years[0], dimension)
    for year in years[1:]:
        df = df.append(import_one(year, dimension))
    #replaces irregular industry codes and converts to integer
    if dimension == 'industry':
        df['industry_code'] = df['industry_code'].str.replace('31-33','31')
        df['industry_code'] = df['industry_code'].str.replace('44-45','44')
        df['industry_code'] = df['industry_code'].str.replace('48-49','48').astype('int32')
    #adds qtrid column
    df = add_qtrid(df)
    return df

def basic_timeline(variable = 'empl', dimension = 'area', recession = 2001, save = False):
    '''
    Produces a dataframe of the indicated recession timeline.

        Parameters: 
            variable (str): determines what economic indicator will be used in the timeline. Must be one of ['month3_emplvl' (employment), 'avg_wkly_wage' (wages), 'qtrly_estabs_count'(firms)]
            dimension (str): dimension of data to import. Must be 'area' or 'industry'. Default = 'area'.
            recession (int or 'full'): recession timeline to compute.
            save (bool): determines if a json file will be generated and saves locally.
    
        Returns: 
            df (pandas dataframe)
            exported json file
    '''
    #creates dataframe of all years in recession
    df = import_all(RECESSION_YEARS[recession], dimension)

    #set indicies, drop unhelpful rows
    if dimension == 'area':
        df = df[~df['area_fips'].str.contains("999")]
        index = ['area_fips', 'area_title']
    elif dimension == 'industry':
        index = ['industry_code', 'industry_title']
        #correct for changes in NAICS classification
        df['industry_title'] = df['industry_code'].apply(lambda x: TITLE[x])
    
    
    #pivots the table to arrange quarters in columns, drops extraneous variables.
    df = df.pivot_table(columns = 'qtrid', values = VARNAME_LONG[variable], index = index, aggfunc = np.sum)
    df = df.reset_index()
    
        #fill nans
    df = df.fillna(0)
    
    #export the data
    if save:
        savepath = filepath(variable = variable, dimension = dimension, recession = recession, filetype = 'json')
            
            # "data/timelines/basic" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json"
        df.to_json(savepath)
    return df

def deflated_timeline(dimension = 'area', variable = 'wage', recession = 2001, save = False):
    if variable != 'wage':
        pass
    loadpath = filepath(variable = 'wage', dimension = dimension, charttype = 'basic', recession = recession, filetype = 'json')
    df = pd.read_json(loadpath)
    for col in df.columns[2:]:
        newcol = col + '_i'
        df[newcol] = cpi.inflate(df[col], int(float(col)- 0.25), 2000)
        df.drop(columns = [col], inplace = True)
        df.rename(columns = {newcol:float(col)}, inplace = True)
    if save:
        savepath = filepath(variable = 'wage', dimension = dimension, charttype = 'basic', recession = recession, filetype = 'json', adjustment = 'deflated')
        df.to_json(savepath)
    return df


def target_timeline(variable = 'empl', dimension = 'area', recession = 2001, save = False, loadjson = False):
    '''
    Produces a dataframe of the indicated recession timeline with derived target variables.
    WARNING: Long processing time required.

    Parameters: 
        variable (str): determines what economic indicator will be used in the timeline. Must be one of ['month3_emplvl' (employment), 'avg_wkly_wage' (wages), 'qtrly_estabs_count'(firms)]
        dimension (str): dimension of data to import. Must be 'area' or 'industry'. Default = 'area'.
        recession (int): recession timeline to compute. Default = 2001. Will pass if 'full'.
        save (bool): determines if a json file will be generated and saves locally. Default = False
        loadjson (bool): determines if basic timeline will be loaded from previously saved file(True) or created anew (False). Existing basic json files will be overwritten if save = True. Default = False

    Returns: 
        df (pandas dataframe)
        exported json file
    '''

    #exits if recession isn't valid
    if recession == 'full':
        pass

    #instantiates a Recession object
    recession = Recession(recession)
    
    #loads the json file if indicated, otherwise calls the basic function to produce the initial timeline
    if loadjson:
        loadpath = filepath(variable = variable, dimension = dimension, charttype= 'basic', recession = recession.event_year, filetype = 'json')
        # filepath =  "data/timelines/basic/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json"
        df = pd.read_json(loadpath)
    else:
        df = basic_timeline(variable = variable, dimension = dimension, recession = recession.event_year, save = save)
    
    #creates a list to store index fields
    if dimension == 'area':
        df = df[~df['area_fips'].str.contains("999")]
        index = ['area_fips', 'area_title']
    elif dimension == 'industry':
        index = ['industry_code', 'industry_title']

    #creates a secondary dataframe with only timeline variables
    df2 = df.drop(columns = index)
    df2 = df2.reset_index()
    
    #drops the index fields so that all columns are free of any type mismatches
    df2 = df2.drop(columns = 'index')
    df2 = df2.fillna(0)

    #specifies the lowest numbers during the recession. Disregards quarters before the recession event. 
    df2['nadir'] = df2.iloc[:,6:].min(axis=1)

    #specifies how many quarters it took before the nadir occured
    df2['nadir_time'] = (df2.iloc[:,6:].idxmin(axis=1).apply(lambda x: df.columns.get_loc(x)))-1
    
    #specifies which quarter the nadir occured.
    df2['nadir_qtr'] =  df2['nadir_time'] / 4 + recession.years[0]
    
    #creates a column to store indices for lookup.
    df2['new'] = [df2.iloc[i].values for i in df.index]
    
    #specifies the highest numbers *before* the nadir.
    df2['pre_peak'] = df2.apply(lambda x: max(x['new'][0:x['nadir_time']]), axis=1)
    
    #specifies the highest numbers *after* the nadir
    df2['post_peak'] = df2.apply(lambda x: max(x['new'][x['nadir_time']:]), axis=1) 
    
    #specifies how many quarters it took before the pre-peak occurred.
    df2['pre_peak_time'] = pd.Series([s[i] for i, s in zip(df2.index, df2['pre_peak'].apply(
        lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x)) + 1
    
    #specifies which quarter the pre-peak occurred.
    df2['pre_peak_qtr'] = df2['pre_peak_time'] / 4 + recession.years[0]

    #specifies which quarter the post-peak occurred.
    df2['post_peak_time'] = pd.Series([s[i] for i, s in zip(df2.index, df2['post_peak'].apply(
        lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x)) + 1

    df2['post_peak_qtr'] = df2['post_peak_time'] / 4 + recession.years[0]

    #PRIMARY TARGET: did the area/industry achieve it's pre-recession peak?
    df2['recovery'] = (df2['post_peak'] >= df2['pre_peak']) *1
    
    #create another dataframe to calculate the # of quarters to recover- only contains recovered datapoints
    df3 = df2[df2['recovery'] == 1]
    
    #creates a column to derive the recovery quarter- list of boolean values
    df3['recovery_list'] = df3.apply(lambda x: (x['new'][x['nadir_time']:] >= x['pre_peak']), axis=1)

    #creates a column for the number or quarters until the results pass the pre-peak high, since the nadir
    df3['recovery_time'] = df3['recovery_list'].apply(lambda x: list(x).index(True)) + 1

    df3['recovery_qtr'] = (df3['nadir_time'] + df3['recovery_time']) / 4 + recession.years[0]

    df3 = df3.reindex(columns = ['recovery_time', 'recovery_qtr'])

    #creates a new dataframe to store derived fields
    df_new = df2[['nadir', 'nadir_qtr', 'nadir_time', 'pre_peak', 'pre_peak_time', 'pre_peak_qtr', 'post_peak', 'post_peak_time', 'post_peak_qtr', 'recovery']]
    
    #adds the recovery quarter column from the third dataframe
    df_new = df_new.join(df3, how = 'left', rsuffix = '_recov')

    #puts the computed points in a dataframe, joins with timeline
    df = df.join(df_new, how = 'outer', rsuffix = '_derive')
    
    #How many quarters did the jobs numbers decline?
    df['decline_time'] = (df['nadir_time'] - df['pre_peak_time'])

    df['growth_time'] = (df['post_peak_time'] - df['nadir_time'])
    
    #Different in before/after jobs numbers
    df['delta'] = df['post_peak'] - df['pre_peak']
    
    #reorders columns for easier organization
    col_order = index
    col_order.extend(recession.quarters)
    col_order.extend(['pre_peak', 'nadir', 'post_peak', 'recovery', 'delta', 'pre_peak_time', 'decline_time', 'nadir_time', 'recovery_time', 'post_peak_time', 'growth_time', 'pre_peak_qtr', 'nadir_qtr', 'recovery_qtr', 'post_peak_qtr'])
    
    #export the data
    if save:
        savepath = filepath(variable = variable, dimension = dimension, charttype= 'target', recession = recession.event_year, filetype = 'json')
        df.to_json(savepath)
    return df

def proportional_timeline(variable = 'month3_emplvl', dimension = 'area', recession = 2001, save = False):
    '''
    Produces a dataframe of the indicated recession timeline as a percentage of the pre-peak. Useful in recreating "scariest chart".

    Does not allow for creating new target timelines (too intensive).

        Parameters: 
            variable (str): determines what economic indicator will be used in the timeline. Must be one of ['month3_emplvl' (employment), 'avg_wkly_wage' (wages), 'qtrly_estabs_count'(firms)]
            dimension (str): dimension of data to import. Must be 'area' or 'industry'. Default = 'area'.
            recession (int or 'full'): recession timeline to compute. Default = 2001. Will exit if recession = 'full'.
            save (bool): determines if a json file will be generated and saved locally. Default = False
    
        Returns: 
            df (pandas dataframe)
            exported json file
    '''

    if recession == 'full':
        pass
    recession = Recession(recession)
    # filepath =  "data/timelines/targets/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json" 
    loadpath = filepath(variable = variable, dimension = dimension, charttype= 'target', recession = recession.event_year, filetype = 'json')
    df = pd.read_json(loadpath)
    df = df.drop(columns =  ['nadir', 'post_peak', 'recovery', 'delta', 'pre_peak_time', 'decline_time', 'nadir_time', 'post_peak_time', 'recovery_time', 'growth_time', 'pre_peak_qtr', 'nadir_qtr', 'recovery_qtr', 'post_peak_qtr'])
    count = -6
    drop_list = ['pre_peak']
    for column in df.columns [2:-1]:
        df[count] = (df[column] - df['pre_peak']) / df['pre_peak']
        count += 1
        drop_list.append(column)
    df.drop(columns = drop_list, inplace= True)
    if save:
        # savepath =  "data/timelines/proportional/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json"
        savepath = filepath(variable = variable, dimension = dimension, charttype= 'proportional', recession = recession.event_year, filetype = 'json')
        df.to_json(savepath) 
    return df

def export_all(basic = False, target = False, proportion = False):
    '''
    Exports json files of all timeline types, across all variables, dimensions, and recessions. Will overwrite any files already saved.

        Parameters: 
            basic (bool): determines if basic timelines will be generated. Default = False
            target (bool): determines if target timelines will be generated. High processing time. Default = False
            proportion (bool): determines if proportional timelines will be generated. Default = False
    
        Returns: 
            exported json files
    '''
    if basic:
        for dimension in ['area', 'industry']: 
            for variable in VARNAME_LONG.keys(): 
                for recession in VALID_RECESSIONS: 
                    basic_timeline(variable = variable, dimension = dimension, recession = recession, save = True)
                basic_timeline(variable = variable, dimension = dimension, recession = 'full', save = True)

    if target:
        for dimension in ['area', 'industry']: 
            for variable in VARNAME_LONG.keys(): 
                for recession in VALID_RECESSIONS:
                    target_timeline(variable = variable, dimension = dimension, recession = recession, save = True, loadjson= not basic)

    if proportion:
        for dimension in ['area', 'industry']:
            for variable in VARNAME_LONG.keys(): 
                for recession in VALID_RECESSIONS:
                    proportional_timeline(variable = variable, dimension = dimension, recession = recession, save = True)                                                                                                                  
