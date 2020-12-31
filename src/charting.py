from src.timeline_dictionaries import *
from src.area_dictionaries import *
from src.industry_dictionaries import *
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import numpy as np

class Vector(object):
    
    def __init__ (self, key, recession, dimension, variable):
        filepath =  "data/timelines/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json" 
        end = end_columns[recession]
        df = pd.read_json(filepath)
        if dimension == 'industry':
            index_col = 'industry_code'
        elif dimension == 'area':
            index_col = 'area_fips'

        self.event_quarter = recession_events[recession]
        self.event_label = events_display[recession]

        recession = Recession(recession)
        self.x = recession.xaxis
        self.y = df








def plot_lines(keys, recession, dimension, variable, markers = ['event', 'nadir', 'pre-peak,', 'post-peak', 'recovery', 'status'], style = 'darkgrid', savepath = 'None'):
    sns.set_style('darkgrid')
    fig, ax = plt.subplots(figsize = (len(recession.quarters),5))
    x = recession.xaxis
    ax.set_title(recession.event_year + ' Recession')
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    if 'event' in markers:
        ax.axvline(x = quarters_display[recession.event_quarter], color = 'black', linewidth = 0.5, alpha = 0.5, label = events_display[recession.event_year])
    if 'nadir' in markers:
        ax.axhline(y = self.nadir_2001, xmin = 'Q1 2000', xmax = 'Q4 2007', 
                    color = 'red', linewidth = .5, alpha = 0.5, label = 'nadir')

    
    for key in list(keys):
        if dimension = 'area':
            if variable = 'month3_emplvl':
                y = recession.area_empl['area_fips'[key]]
            if variable = 'avg_wkly_wage':
                y = recession.area_wage['area_fips'[key]]
            if variable = 'qtrly_estabs_count':
                y = recession.area_firm['area_fips'[key]]
        if dimension = 'industry':
            if variable = 'month3_emplvl':
                y = recession.indus_empl['area_fips'[key]]
            if variable = 'avg_wkly_wage':
                y = recession.indus_wage['area_fips'[key]]
            if variable = 'qtrly_estabs_count':
                y = recession.indus_firm['area_fips'[key]]

    def plot_2001(self):
        y = self.y_2001
        ax.plot(x,y, color = 'green', linewidth = 1, alpha = 0.8)
        ax.axhline(y = self.nadir_2001, xmin = 'Q1 2000', xmax = 'Q4 2007', 
                    color = 'red', linewidth = .5, alpha = 0.5, label = 'nadir')
        ax.axhline(y = self.pre_peak_2001, xmin = 'Q1 2000', xmax = 'Q4 2007',
                    color = 'blue', linewidth = .5, alpha = .5, label = 'pre-recession-peak')
        
        ax.axvline(x = 'Q3 2001', color = 'black', linewidth = 0.5, alpha = 0.5, label = '09/11/2001')
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('src/static/images/plot_2001.png')
        return fig, ax