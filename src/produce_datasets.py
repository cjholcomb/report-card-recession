import pandas as pd
import numpy as np
import cpi
import os
from statistics import mean

from src.constants import *
from src.classes import *
# from recessions import Recession
# from industries import industry_titles

census_lookup = {
    2010:{'filetype':'.csv', 
        'rename_cols': {'POPESTIMATE2010': 2010, 'POPESTIMATE2011': 2011, 'POPESTIMATE2012': 2012, 'POPESTIMATE2013': 2013, 'POPESTIMATE2014': 2014,'POPESTIMATE2015': 2015, 'POPESTIMATE2016': 2016, 'POPESTIMATE2017': 2017, 'POPESTIMATE2018': 2018, 'POPESTIMATE2019': 2019},
        'drop_cols': ['SUMLEV', 'REGION', 'DIVISION', 'STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'CENSUS2010POP', 'ESTIMATESBASE2010', 'NPOPCHG_2010', 'NPOPCHG_2011', 'NPOPCHG_2012', 'NPOPCHG_2013', 'NPOPCHG_2014', 'NPOPCHG_2015', 'NPOPCHG_2016', 'NPOPCHG_2017', 'NPOPCHG_2018', 'NPOPCHG_2019', 'BIRTHS2010', 'BIRTHS2011', 'BIRTHS2012', 'BIRTHS2013', 'BIRTHS2014', 'BIRTHS2015', 'BIRTHS2016', 'BIRTHS2017', 'BIRTHS2018', 'BIRTHS2019', 'DEATHS2010', 'DEATHS2011', 'DEATHS2012', 'DEATHS2013', 'DEATHS2014', 'DEATHS2015', 'DEATHS2016', 'DEATHS2017', 'DEATHS2018', 'DEATHS2019', 'NATURALINC2010', 'NATURALINC2011', 'NATURALINC2012', 'NATURALINC2013', 'NATURALINC2014', 'NATURALINC2015', 'NATURALINC2016', 'NATURALINC2017', 'NATURALINC2018', 'NATURALINC2019', 'INTERNATIONALMIG2010', 'INTERNATIONALMIG2011', 'INTERNATIONALMIG2012', 'INTERNATIONALMIG2013', 'INTERNATIONALMIG2014', 'INTERNATIONALMIG2015', 'INTERNATIONALMIG2016', 'INTERNATIONALMIG2017', 'INTERNATIONALMIG2018', 'INTERNATIONALMIG2019', 'DOMESTICMIG2010', 'DOMESTICMIG2011', 'DOMESTICMIG2012', 'DOMESTICMIG2013', 'DOMESTICMIG2014', 'DOMESTICMIG2015', 'DOMESTICMIG2016', 'DOMESTICMIG2017', 'DOMESTICMIG2018', 'DOMESTICMIG2019', 'NETMIG2010', 'NETMIG2011', 'NETMIG2012', 'NETMIG2013', 'NETMIG2014', 'NETMIG2015', 'NETMIG2016', 'NETMIG2017', 'NETMIG2018', 'NETMIG2019', 'RESIDUAL2010', 'RESIDUAL2011', 'RESIDUAL2012', 'RESIDUAL2013', 'RESIDUAL2014', 'RESIDUAL2015', 'RESIDUAL2016', 'RESIDUAL2017', 'RESIDUAL2018', 'RESIDUAL2019', 'GQESTIMATESBASE2010', 'GQESTIMATES2010', 'GQESTIMATES2011', 'GQESTIMATES2012', 'GQESTIMATES2013', 'GQESTIMATES2014', 'GQESTIMATES2015', 'GQESTIMATES2016', 'GQESTIMATES2017', 'GQESTIMATES2018', 'GQESTIMATES2019', 'RBIRTH2011', 'RBIRTH2012', 'RBIRTH2013', 'RBIRTH2014', 'RBIRTH2015', 'RBIRTH2016', 'RBIRTH2017', 'RBIRTH2018', 'RBIRTH2019', 'RDEATH2011', 'RDEATH2012', 'RDEATH2013', 'RDEATH2014', 'RDEATH2015', 'RDEATH2016', 'RDEATH2017', 'RDEATH2018', 'RDEATH2019', 'RNATURALINC2011', 'RNATURALINC2012', 'RNATURALINC2013', 'RNATURALINC2014', 'RNATURALINC2015', 'RNATURALINC2016', 'RNATURALINC2017', 'RNATURALINC2018', 'RNATURALINC2019', 'RINTERNATIONALMIG2011', 'RINTERNATIONALMIG2012', 'RINTERNATIONALMIG2013', 'RINTERNATIONALMIG2014', 'RINTERNATIONALMIG2015', 'RINTERNATIONALMIG2016', 'RINTERNATIONALMIG2017', 'RINTERNATIONALMIG2018', 'RINTERNATIONALMIG2019', 'RDOMESTICMIG2011', 'RDOMESTICMIG2012', 'RDOMESTICMIG2013', 'RDOMESTICMIG2014', 'RDOMESTICMIG2015', 'RDOMESTICMIG2016', 'RDOMESTICMIG2017', 'RDOMESTICMIG2018', 'RDOMESTICMIG2019', 'RNETMIG2011', 'RNETMIG2012', 'RNETMIG2013', 'RNETMIG2014', 'RNETMIG2015', 'RNETMIG2016', 'RNETMIG2017', 'RNETMIG2018', 'RNETMIG2019'],
        'total_row': {'area_fips':'US000', 2010: 309011475, 2011: 311584047, 2012: 314043885, 2013: 316400538, 2014: 318673411, 2015: 320878310, 2016: 323015995, 2017: 325084756, 2018: 327096265, 2019: 329064917}
        },
    2000:{'filetype':'.csv',
        'rename_cols': {'POPESTIMATE2000': 2000, 'POPESTIMATE2001': 2001, 'POPESTIMATE2002': 2002, 'POPESTIMATE2003': 2003, 'POPESTIMATE2004': 2004,'POPESTIMATE2005': 2005, 'POPESTIMATE2006': 2006, 'POPESTIMATE2007': 2007, 'POPESTIMATE2008': 2008, 'POPESTIMATE2009': 2009},
        'drop_cols': ['SUMLEV', 'REGION', 'DIVISION', 'STATE', 'COUNTY', 'STNAME', 'CTYNAME', 'ESTIMATESBASE2000', 'CENSUS2010POP', 'POPESTIMATE2010'],
        'total_row': {'area_fips':'US000', 2000: 281710909, 2001: 284607993, 2002: 287279318, 2003: 289815562, 2004: 292354658, 2005: 294993511, 2006: 297758969, 2007: 300608429, 2008: 303486012, 2009: 306307567}
    },
    1990:{'filename':'1990.txt',
        'header': 17,
        'data_rows': [[19, 3212]],
        'final_row': 32009,
        'fips_convert': 'County',
        'drop_cols': ['4/1/1990', 'Area Name', 'County', '7/1/2000'],
        'rename_cols': {'7/1/1990': 1990, '7/1/1991': 1991, '7/1/1992': 1992, '7/1/1993': 1993, '7/1/1994': 1994, '7/1/1995': 1995, '7/1/1996': 1996, '7/1/1997': 1997, '7/1/1998': 1998, '7/1/1999': 1999}
        },
    1980:{'filename':'1980.txt',
        'header':24,
        'data_rows': [[26, 94], [169, 213], [261, 277], [299, 375], [457, 520], [589, 653], [723, 732], [747, 751], [761, 763], [771, 839], [913, 1074], [1241, 1247], [1259, 1304], [1355, 1458], [1567, 1660], [1759, 1860], [1967, 2073], [2185, 2306], [2433, 2508], [2589, 2606], [2629, 2655], [2687, 2702], [2723, 2808], [2899, 2990], [3087, 3171], [3261, 3379], [3503, 3564], [3631, 3725], [3825, 3843], [3867, 3878], [3895, 3917], [3945, 3979], [4019, 4082], [4151, 4252], [4359, 4414], [4475, 4564], [4659, 4737], [4821, 4858], [4901, 4970], [5045, 5051], [5063, 5110], [5163, 5230], [5303, 5399], [5501, 5758], [6021, 6051], [6087, 6102], [6123, 6278], [6440, 6480], [6526, 6582], [6644, 6717], [6796, 6820]],
        'final_row': 6847,
        'fips_convert': 'Code',
        'total_row': {'Code': 0, 'Area Name':'U.S. Total', '1980':226542250, '1981':229465744, '1982':231664432, '1983':233792014, '1984':235824908, 'area_fips':'USOOO'},
        'drop_cols': ['Code', 'Area Name'],
        'rename_cols': {}
        },
    1985:{'filename':'1980.txt',
        'header': 96,
        'data_rows':[[98, 166], [216, 258], [280, 296], [378, 454], [523, 586], [656, 720], [735, 744], [754, 758], [766, 768], [842, 910], [1077, 1238], [1250, 1256], [1307, 1352], [1461, 1564], [1663, 1756], [1863, 1964], [2076, 2182], [2309, 2430], [2511, 2586], [2609, 2626], [2658, 2684], [2705, 2720], [2811, 2896], [2993, 3084], [3174, 3258], [3382, 3500], [3567, 3628], [3728, 3822], [3846, 3864], [3881, 3892], [3920, 3942], [3982, 4016], [4085, 4148], [4255, 4356], [4417, 4472], [4567, 4656], [4740, 4818], [4861, 4898], [4973, 5042], [5054, 5060], [5113, 5160], [5233, 5300], [5402, 5498], [5761, 6018], [6054, 6084], [6105, 6120], [6281, 6437], [6483, 6523], [6585, 6641], [6720, 6793], [6823, 6847]],
        'final_row': 6847,
        'fips_convert': 'Code',
        'total_row':{'Code': 0, 'Area Name':  'U.S. Total', '1985':237923734, '1986':240132831, '1987':242288936, '1988':244499004, '1989':246819222, 'area_fips':'USOOO'},
        'drop_cols': ['Code', 'Area Name'],
        'rename_cols': {}
        },
    1975:{'filename':'1970.txt',
        'header': 100,
        'data_rows': [[102, 170], [213, 249], [272, 288], [370, 446], [516, 579], [649, 713], [728, 737], [747, 751], [759, 761], [835, 903], [1070, 1231], [1242, 1247], [1298, 1343], [1452, 1555], [1654, 1747], [1854, 1955], [2067, 2173], [2300, 2421], [2500, 2572], [2595, 2612], [2644, 2670], [2691, 2706], [2797, 2882], [2979, 3070], [3160, 3244], [3368, 3486], [3553, 3614], [3714, 3808], [3832, 3850], [3867, 3878], [3906, 3928], [3968, 4002], [4071, 4134], [4241, 4342], [4402, 4456], [4552, 4641], [4725, 4803], [4846, 4883], [4958, 5027], [5039, 5045], [5098, 5145], [5218, 5285], [5387, 5483], [5744, 5999], [6035, 6065], [6086, 6101], [6259, 6412], [6458, 6498], [6560, 6616], [6695, 6768], [6798, 6822]],
        'final_row': 6847,
        'fips_convert': 'Code',
        'total_row':{'Code': 0, 'Area Name':  'U.S. Total', '1975':215464000, '1976':217562000, '1977':219759000, '1978':222095000, '1979':224567000,  'area_fips':'USOOO'},
        'drop_cols': ['Code', 'Area Name'],
        'rename_cols':{}
        }
    }

def create_filepaths(path = 'basic', dimension = 'area', variable = 'empl'):
    if not os.path.exists('data/timelines'):
        os.mkdir('data/timelines')

    if path in ['deflated', 'smoothed']:
        if not os.path.exists('data/timelines/adjusted'):
            os.mkdir('data/timelines/adjusted')
        if not os.path.exists('data/timelines/adjusted/' + path):
            os.mkdir('data/timelines/adjusted/' + path)            
        if not os.path.exists('data/timelines/adjusted/' + path + '/' + dimension):
            os.mkdir('data/timelines/adjusted/' + path + '/' + dimension)
        if not os.path.exists('data/timelines/adjusted/' + path + '/' + dimension + '/' + variable):
            os.mkdir('data/timelines/adjusted/' + path + '/' + dimension + '/' + variable)

    if path in ['basic', 'proportional', 'target']:
        if not os.path.exists('data/timelines/' + path):
            os.mkdir('data/timelines/' + path)
        if not os.path.exists('data/timelines/' + path + '/' + dimension):
            os.mkdir('data/timelines/' + path + '/' + dimension)
        if not os.path.exists('data/timelines/' + path + '/' + dimension + '/' + variable):
            os.mkdir('data/timelines/' + path + '/' + dimension + '/' + variable)

    if path == 'population':
        if not os.path.exists('data/timelines/population'):
            os.mkdir('data/timelines/population')

def txt_cleanup(df, fips_convert):
    drop_rows = []
    for index, row in df.iterrows():
        if pd.isnull(row[fips_convert]):
            # df.iloc[index - 1,1] = df.iloc[index - 1,1] + ' ' + df.iloc[index,1]
            for num in range(2, 7):
                df.iloc[index - 1,num] = df.iloc[index,num]
            drop_rows.append(index)
    df.drop(drop_rows, axis = 0, inplace= True)
    return df

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
            source (str): Data source to be downloaded from
        
        Returns:
            df (pandas dataframe)
    '''
    filepath = 'data/source_files/QCEW/' +  dimension + '_QCEW/' + str(year) + '.csv'
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
    if dimension == 'industry' and year >= 1990:
        df['industry_code'] = df['industry_code'].str.replace('31-33','31')
        df['industry_code'] = df['industry_code'].str.replace('44-45','44')
        df['industry_code'] = df['industry_code'].str.replace('48-49','48').astype('int32')
    #adds qtrid column
    df = add_qtrid(df)
    return df

def save_json(df, savepath, override = False):
    if os.path.exists(savepath) and override ==  False:
        print(savepath + ' already exists.')
        pass
    else:
        df.to_json(savepath)
        print(savepath + ' saved.')

def basic_timeline(variable = 'empl', dimension = 'area', recession = 2001, save = False, override = False):
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
        
        df['industry_title'] = df['industry_code'].apply(lambda x: TITLE[int(x)])
    
    
    #pivots the table to arrange quarters in columns, drops extraneous variables.
    df = df.pivot_table(columns = 'qtrid', values = VARNAME_LONG[variable], index = index, aggfunc = np.sum)
    df = df.reset_index()
    
    #fill nans
    df = df.fillna(0)
    
    #export the data
    if save:
        create_filepaths(path = 'basic', dimension= dimension, variable = variable)
        savepath = filepath(variable = variable, dimension = dimension, recession = recession, filetype = 'json')
        save_json(df, savepath = savepath, override = override)
    return df

def deflated_timeline(dimension = 'area', recession = 2001, save = False, override = False):
    loadpath = filepath(variable = 'wage', dimension = dimension, data = 'basic', recession = recession, filetype = 'json')
    df = pd.read_json(loadpath)
    for col in df.columns[2:]:
        newcol = col + '_i'
        df[newcol] = cpi.inflate(df[col], int(float(col)- 0.25), 2000)
        df.drop(columns = [col], inplace = True)
        df.rename(columns = {newcol:float(col)}, inplace = True)
    if save:
        create_filepaths(path = 'deflated', dimension= dimension, variable = 'wage')
        savepath = filepath(variable = 'wage', dimension = dimension, recession = recession, data = 'deflated', adjustment= True, filetype = 'json')
        save_json(df, savepath = savepath, override = override)
    return df

def smoothed_timeline(variable = 'empl', dimension = 'area', recession = 2001, save = False, override = False):
    
    #adds a year to the beginning of the normal timeline
    years = RECESSION_YEARS[recession]
    years.append(min(years) - 1)
    years.sort()
    df = import_all(years, dimension)
    if dimension == 'area':
        df = df[~df['area_fips'].str.contains("999")]
        index = ['area_fips', 'area_title']
    elif dimension == 'industry':
        index = ['industry_code', 'industry_title']
        #correct for changes in NAICS classification
        df['industry_title'] = df['industry_code'].apply(lambda x: TITLE[x])
    df = df.pivot_table(columns = 'qtrid', values = VARNAME_LONG[variable], index = index, aggfunc = np.sum)
    df = df.reset_index()
        
    #fill nans
    df = df.fillna(0)

    #averages the previous 4 quarters
    for col in df.columns[6:]:
        newcol =  str(col) + '_s'
        index = df.columns.get_loc(col)
        interval = df.iloc[:,(index-3):index]
        df[newcol] = interval.mean(axis=1)
        df.drop(columns = [col], inplace = True)
        df.rename(columns = {newcol:float(col)}, inplace = True)
    
    #removes the initial year
    df.drop(columns = list(df.columns[2:6]), inplace = True)

    #saves the json file
    if save:
        create_filepaths(path = 'smoothed', dimension= dimension, variable = variable)
        savepath = filepath(variable = variable, dimension = dimension, recession = recession, data = 'smoothed', adjustment= True, filetype = 'json')
        save_json(df, savepath = savepath, override = override)
    return df
    
def target_timeline(variable = 'empl', dimension = 'area', recession = 2001, save = False, loadjson = False, override = False):
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
        loadpath = filepath(variable = variable, dimension = dimension, data = 'basic', recession = recession.event_year, filetype = 'json')
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
        create_filepaths(path = 'target', dimension= dimension, variable = variable)
        savepath = filepath(variable = variable, dimension = dimension, recession = recession.event_year, data = 'target', filetype = 'json')
        save_json(df, savepath = savepath, override = override)
    return df

def proportional_timeline(variable = 'month3_emplvl', dimension = 'area', recession = 2001, save = False, override = False):
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
    loadpath = filepath(variable = variable, dimension = dimension, data= 'target', recession = recession.event_year, filetype = 'json')
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
        create_filepaths(path = 'proportional', dimension= dimension, variable = variable)
        savepath = filepath(variable = variable, dimension = dimension, recession = recession.event_year, data = 'proportional', adjustment= False, filetype = 'json')
        save_json(df, savepath = savepath, override = override)
    return df

def population_timeline(decades = [1970, 1980, 1990, 2000, 2010], save = False, override = False):
    loadpath = 'data/source_files/census/county/'
    df_master = None
    if (1980 in decades) & (1985 not in decades):
        decades.append(1985)
    if 1970 in decades:
        if 1975 not in decades:
            decades.append(1975)
        decades.remove(1970)
    decades.sort(reverse =  True)
    for decade in decades:
        lookup = census_lookup[decade]
        if int(decade) >= 2000:
            df = pd.read_csv(loadpath + str(decade) + lookup['filetype'], encoding = 'ISO-8859-1')
            df['area_fips'] = df['STATE'].apply(lambda x: str(x).zfill(2)) + df['COUNTY'].apply(lambda x: str(x).zfill(3))
        else:
            keeprows = [lookup['header']]
            for rows in lookup['data_rows']:
                keeprows.extend(list(range(rows[0], rows[1] + 1 )))
            skiprows = [x for x in range(0, lookup['final_row']) if x not in keeprows]
            df = pd.read_fwf(loadpath + lookup['filename'], skiprows = skiprows, delim_whitepace = True)
            if decade <= 1985:
                df = txt_cleanup(df, lookup['fips_convert'])
                df['area_fips'] = df[lookup['fips_convert']].apply(lambda x: str(int(x)).zfill(5))
                df =  df.append(lookup['total_row'], ignore_index =True)
            else:
                df['area_fips'] = df[lookup['fips_convert']].apply(lambda x: '{:<06}'.format(x[2:]))
                df['area_fips'] = df['area_fips'].apply(lambda x: str(x)[1:])
                df.iloc[0,14] = 'US000'
                df.drop(df.tail(1).index, inplace =  True)
        df.drop(columns = lookup['drop_cols'], inplace = True)
        df.rename(columns = lookup['rename_cols'], inplace = True)
        if int(decade) >= 2000:
            df = df.append(lookup['total_row'], ignore_index = True)
        df.set_index('area_fips', inplace = True)    
        df.rename(columns = dict(zip(list(df.columns), list(map(int, df.columns)))), inplace = True)
        if df_master is not None:
            df_master.reset_index(inplace = True)
            df_master = df_master.join(df, on = 'area_fips', how ='outer', lsuffix= '_left', rsuffix= '_right')
            # print(df_master)
            df_master.set_index('area_fips', inplace= True)
        else:
            df_master = df
        df_master = df_master[list(range(np.min(df_master.columns), np.max(df_master.columns) + 1))]
    if save:
        create_filepaths(path = 'population')
        savepath = 'data/timelines/population/population.json'
        save_json(df_master, savepath = savepath, override = override)
    return df_master

def export_all(basic = False, deflated = False, smoothed = False,  target = False, proportional = False, population = False, override = False):
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

    if deflated:
        for dimension in ['area', 'industry']: 
            for recession in VALID_RECESSIONS:
                deflated_timeline(dimension= dimension, recession = recession, save = True)

    if smoothed:
        for dimension in ['area', 'industry']: 
            for variable in VARNAME_LONG.keys(): 
                for recession in VALID_RECESSIONS: 
                    smoothed_timeline(variable = variable, dimension = dimension, recession = recession, save = True)
                smoothed_timeline(variable = variable, dimension = dimension, recession = 'full', save = True)

    if target:
        for dimension in ['area', 'industry']: 
            for variable in VARNAME_LONG.keys(): 
                for recession in VALID_RECESSIONS:
                    target_timeline(variable = variable, dimension = dimension, recession = recession, save = True, loadjson= not basic)

    if proportional:
        for dimension in ['area', 'industry']:
            for variable in VARNAME_LONG.keys(): 
                for recession in VALID_RECESSIONS:
                    proportional_timeline(variable = variable, dimension = dimension, recession = recession, save = True)

    if population:
        for recession in VALID_RECESSIONS:
            population_timeline(save = True)                                                                                                                  
