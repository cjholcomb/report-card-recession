import pandas as pd
import numpy as np

from recessions import recessions_int, dim_abbr, var_abbr

#lists of variables to drop during timeline construction
timeline2001_dropcols = [2000.25, 2000.5, 2000.75, 2001.0, 2001.25, 2001.5, 2001.75, 2002.0, 2002.25, 2002.5, 2002.75, 2003.0, 2003.25, 2003.5, 2003.75, 2004.0, 2004.25, 2004.5, 2004.75, 2005.0, 2005.25, 2005.5, 2005.75, 2006.0, 2006.25, 2006.5, 2006.75, 2007.0, 2007.25, 2007.5, 2007.75, 2008.0, 'nadir', 'nadir_qtr', 'new', 'pre_peak', 'post_peak','pre_peak_qtr', 'post_peak_qtr', 'recovery', 'recovery_list']
timeline2008_dropcols = [2007.25, 2007.5, 2007.75, 2008.0, 2008.25, 2008.5, 2008.75, 2009.0, 2009.25, 2009.5, 2009.75, 2010.0, 2010.25, 2010.5, 2010.75, 2011.0, 2011.25, 2011.5, 2011.75, 2012.0, 2012.25, 2012.5, 2012.75, 2013.0, 2013.25, 2013.5, 2013.75, 2014.0, 2014.25, 2014.5, 2014.75, 2015.0, 2015.25, 2015.5, 2015.75, 2016.0, 2016.25, 2016.5, 2016.75, 2017.0, 2017.25, 2017.5, 2017.75, 2018.0, 2018.25, 2018.5, 2018.75, 2019.0, 2019.25, 2019.5, 2019.75, 2020.0, 'nadir', 'nadir_qtr', 'new', 'pre_peak', 'post_peak','pre_peak_qtr', 'post_peak_qtr', 'recovery', 'recovery_list']
timelinefull_dropcols = [2000.25, 2000.5, 2000.75, 2001.0, 2001.25, 2001.5, 2001.75, 2002.0, 2002.25, 2002.5, 2002.75, 2003.0, 2003.25, 2003.5, 2003.75, 2004.0, 2004.25, 2004.5, 2004.75, 2005.0, 2005.25, 2005.5, 2005.75, 2006.0, 2006.25, 2006.5, 2006.75, 2007.0, 2007.25, 2007.5, 2007.75, 2008.0, 2008.25, 2008.5, 2008.75, 2009.0, 2009.25, 2009.5, 2009.75, 2010.0, 2010.25, 2010.5, 2010.75, 2011.0, 2011.25, 2011.5, 2011.75, 2012.0, 2012.25, 2012.5, 2012.75, 2013.0, 2013.25, 2013.5, 2013.75, 2014.0, 2014.25, 2014.5, 2014.75, 2015.0, 2015.25, 2015.5, 2015.75, 2016.0, 2016.25, 2016.5, 2016.75, 2017.0, 2017.25, 2017.5, 2017.75, 2018.0, 2018.25, 2018.5, 2018.75, 2019.0, 2019.25, 2019.5, 2019.75, 2020.0, 'nadir', 'nadir_qtr', 'new', 'pre_peak', 'post_peak','pre_peak_qtr', 'post_peak_qtr', 'recovery', 'recovery_list']

#schema for importing dataframe
schema_dict = { 'area_fips':str,  'own_code':str,  'industry_code':str,  'agglvl_code':str,  'size_code':str,  'year':int,  'qtr':int,  'disclosure_code':str, 'area_title':str,  'own_title':str,  'industry_title':str,  'agglvl_title':str,  'size_title':str,  'qtrly_estabs':int,  'month1_emplvl':int,  'month2_emplvl':int,  'month3_emplvl':int,  'total_qtrly_wages':int,  'taxable_qtrly_wages':int,  'qtrly_contributions':int,  'avg_wkly_wage':int,  'lq_disclosure_code':str,  'lq_qtrly_estabs':float,  'lq_month1_emplvl':float,  'lq_month1_emplv2':float,  'lq_month1_emplv3':float,  'lq_total_qtrly_wages':float,  'lq_taxable_qtrly_wages':float,  'lq_qrtly_contributions':float,  'oty_disclosure_code':str,  'oty_qtrly_estabs':int,  'oty_qtrly_estabs_pct_chg':float,  'oty_month1_emplvl_chg':int,  'oty_month1_emplvl_pct_chg':float,  'oty_month2_emplv_chg':int,  'oty_month2_emplvl_pct_chg':float,  'oty_month3_emplvl_chg':int,  'oty_month3_emplvl_pct_chg':float,  'oty_total_qtrly_wages_chg':int,  'oty_total_qtrly_wages_pct_chg':float,  'oty_taxable_qtrly_wages_chg':int,  'oty_taxable_qtrly_wages_pct_chg':float,  'oty_qrtly_contributions_chg':int,  'oty_qrtly_contributions_pct_chg':float,  'oty_avg_wkly_wage_chg':int,  'oty_avg_wkly_wage_pct_chg':float} 

#unused columns from QCEW
drop_columns = ['own_code',  'size_code',  'disclosure_code',  'own_title',  'size_title',  'lq_disclosure_code', 'oty_disclosure_code',  'oty_month1_emplvl_chg',  'oty_month2_emplvl_chg',  'oty_month3_emplvl_chg',  'oty_total_qtrly_wages_chg',  'oty_taxable_qtrly_wages_chg',  'oty_qtrly_contributions_chg',  'oty_avg_wkly_wage_chg',  'lq_qtrly_estabs_count',  'lq_month1_emplvl',  'lq_month2_emplvl',  'lq_month3_emplvl',  'lq_total_qtrly_wages',  'lq_taxable_qtrly_wages',  'lq_qtrly_contributions',  'oty_qtrly_estabs_count_chg',  'oty_qtrly_estabs_count_pct_chg',  'oty_month1_emplvl_pct',  'oty_month2_emplvl_pct',  'oty_month3_emplvl_pct',  'oty_total_qtrly_wages_pct',  'oty_taxable_qtrly_wages_chg',  'oty_qtrly_contributions_pct',  'oty_avg_wkly_wage_pct',  'oty_taxable_qtrly_wages_chg.1',  'lq_avg_wkly_wage',  'taxable_qtrly_wages',  'qtrly_contributions']


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
    for column in drop_columns:
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

def create_timeline(variable = 'month3_emplvl', dimension = 'area', recession = 2001, targets = False, save = False):
    '''
    Produces a dataframe of the indicated recession timeline.

        Parameters: 
            variable (str): determines what economic indicator will be used in the timeline. Must be one of ['month3_emplvl' (employment), 'avg_wkly_wage' (wages), 'qtrly_estabs_count'(firms)]
            dimension (str): dimension of data to import. Must be 'area' or 'industry'. Default = 'area'.
            recession (int or 'full'): recession timeline to compute.
            targets (bool): determines if derived variables will be computed. Greatly increases processing time.
            save (bool): determines if a json file will be generated and saves locally.
    
        Returns: 
            df (pandas dataframe)
            exported json file
    '''
    #creates dataframe of all years in recession
    df = import_all(recessions_int[recession], dimension)

    #set indicies, drop unhelpful rows
    if dimension == 'area':
        df = df[~df['area_fips'].str.contains("999")]
        index = ['area_fips', 'area_title']
    elif dimension == 'industry':
        index = ['industry_code', 'industry_title']
    
    #pivots the table to arrange quarters in columns, drops extraneous variables.
    df = df.pivot_table(columns = 'qtrid', values = variable, index = index, aggfunc = np.sum)
    df = df.reset_index()
    
    #fill nans
    df = df.fillna(0)

    #derives targets and associated variables
    if targets:
        #creates a secondary dataframe with only timeline variables
        df2 = df.drop(columns = index)
        df2 = df2.reset_index()
        
        #drops the index so that all calculations are free of any type mismatches
        df2 = df2.drop(columns = 'index')
        df2 = df2.fillna(0)

        #specifies the lowest numbers during the recession. Disregards quarters before the recession event. 
        df2['nadir'] = df2.iloc[:,6:].min(axis=1)

        #specifies which quarter the nadir occured.
        df2['nadir_qtr'] = (df2.iloc[:,6:].idxmin(axis=1).apply(lambda x: df.columns.get_loc(x)))-1
        
        #creates a column to store indices for lookup.
        df2['new'] = [df2.iloc[i].values for i in df.index]
        
        #specifies the highest numbers *before* the nadir.
        df2['pre_peak'] = df2.apply(lambda x: max(x['new'][0:x['nadir_qtr']]), axis=1)
        
        #specifies the highest numbers *after* the nadir
        df2['post_peak'] = df2.apply(lambda x: max(x['new'][x['nadir_qtr']:]), axis=1) 
        
        #specifies which quarter the pre-peak occurred.
        df2['pre_peak_qtr'] = pd.Series([s[i] for i, s in zip(df2.index, df2['pre_peak'].apply(
            lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                    .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x)) + 1
        
        #specifies which quarter the post-peak occurred.
        df2['post_peak_qtr'] = pd.Series([s[i] for i, s in zip(df2.index, df2['post_peak'].apply(
            lambda x: [i for i in (df2.iloc[:,0:-6] == x)
                    .idxmax(axis=1)]))]).apply(lambda x: df2.columns.get_loc(x)) + 1

        #PRIMARY TARGET: did the area/industry achieve it's pre-recession peak?
        df2['recovery'] = (df2['post_peak'] >= df2['pre_peak']) *1
        
        #create another dataframe to calculate the # of quarters to recover- only contains recovered datapoints
        df3 = df2[df2['recovery'] == 1]
        
        #creates a column to derive the recovery quarter- list of boolean values
        df3['recovery_list'] = df3.apply(lambda x: (x['new'][x['nadir_qtr']:] >= x['pre_peak']), axis=1)

        #creates a column for the number or quarters until the results pass the pre-peak high, since the nadir
        df3['recovery_qtr'] = df3['recovery_list'].apply(lambda x: list(x).index(True)) + 1

        #drops all redunant fields from the third dataframe
        if recession == 2001:
            dropcols = timeline2001_dropcols
        elif recession == 2008:
            dropcols = timeline2008_dropcols
        elif recession == 'full':
            dropcols = timelinefull_dropcols
        df3 = df3.drop(columns = dropcols)

        #creates a new dataframe to store derived fields
        df_new = df2[['nadir', 'nadir_qtr', 'pre_peak', 'pre_peak_qtr', 'post_peak', 'post_peak_qtr', 'recovery']]

        #adds the recovery quarter column from the third dataframe
        df_new = df_new.join(df3, how = 'left', rsuffix = '_recov')

        #puts the computed points in a dataframe, joins with timeline
        df = df.join(df_new, how = 'outer', rsuffix = '_derive')
        
        #How many quarters did the jobs numbers decline?
        df['decline'] = (df['nadir_qtr'] - df['pre_peak_qtr'])
        
        #Different in before/after jobs numbers
        df['delta'] = df['post_peak'] - df['pre_peak']
    
        #export the data
        if save:
            savepath = "data/timelines_w_targets/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json"
            df.to_json(savepath)

    else:
        #export the data
        if save:
            savepath = "data/timelines/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json"
            df.to_json(savepath)

    return df

def export_all(targets = False):
    for dimension in ['area', 'industry']: 
        for variable in ['month3_emplvl', 'avg_wkly_wage', 'qtrly_estabs_count']: 
            for recession in [2001, 2008, 'full']: 
                create_timeline(variable = variable, dimension = dimension, recession = recession, save = True, targets= targets)                                                                                                              