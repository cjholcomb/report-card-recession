from src.timeline_dictionaries import *
from src.area_dictionaries import *
from src.industry_dictionaries import *
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np


class Vector(object):
    
    def __init__ (self, key, recession, dimension, variable, chart = False, style = 'darkgrid'):
        filepath =  "data/timelines/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json" 
        end = end_columns[recession]
        df = pd.read_json(filepath)
        if dimension == 'industry':
            index_col = 'industry_code'
            index_title = 'industry_title'
        elif dimension == 'area':
            index_col = 'area_fips'
            index_title = 'area_title'
        df = df.set_index(index_col)
        self.event_quarter = recession_events[recession]
        self.event_label = events_display[recession]
        recession = Recession(recession)
        self.x = recession.xaxis
        self.y = df.loc[key][1:end]
        self.label = df[index_title].loc[key]
        self.nadir = df['nadir'].loc[key]
        self.nadir_qtr = df['nadir_qtr'].loc[key] / 4 + recession.years[0]
        self.pre_peak = df['pre_peak'].loc[key]
        self.pre_peak_qtr = df['pre_peak_qtr'].loc[key] / 4 + recession.years[0]
        self.post_peak = df['post_peak'].loc[key]
        self.post_peak_qtr = df['post_peak_qtr'].loc[key] / 4 + recession.years[0]
        self.recovery_qtr = (df['nadir_qtr'].loc[key] + df['recovery_qtr'].loc[key]) / 4 + recession.years[0]
        self.decline = df['decline'].loc[key]
        self.delta = df['delta'].loc[key]
        if chart:
            fig, ax = plt.subplots(figsize = (15, 4))
            ax.plot(self.x,self.y, color = 'green', linewidth = 1, alpha = 0.8, label = self.label)
            self.ax = ax
            sns.set_style(style)
            ax.axhline(y = self.nadir, xmin = self.x[0], xmax = self.x[-1], color = 'red', linewidth = .5, alpha = 0.5, label = 'nadir: ' + str(quarters_display[self.nadir_qtr]))
            ax.axhline(y = self.pre_peak, xmin = self.x[0], xmax = self.x[-1], color = 'blue', linewidth = .5, alpha = .5, label = 'pre-recession-peak: ' + str(quarters_display[self.pre_peak_qtr]))
            ax.axhline(y = self.post_peak, xmin = self.x[0], xmax = self.x[-1], color = 'blue', linewidth = .5, alpha = .5, label = 'post-recession-peak: ' + str(quarters_display[self.post_peak_qtr]))
            ax.axvline(x = quarters_display[self.event_quarter], color = 'black', linewidth = 0.5, alpha = 0.5, label = self.event_label)
            ax.axvline(x = quarters_display[self.recovery_qtr], color = 'purple', linewidth = 0.5, alpha = 0.5, label = 'recovery: ' + str(quarters_display[self.recovery_qtr]))
            ax.set_title(str(recession.event_year) + ' Recession')
            ax.tick_params(axis='both', which='major', labelsize=10)
            ax.tick_params(axis='both', which='minor', labelsize=10)
            ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
            ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
            ax.legend(fancybox = True, borderaxespad=0)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

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
        if dimension == 'area':
            if variable == 'month3_emplvl':
                y = recession.area_empl['area_fips'[key]]
            if variable == 'avg_wkly_wage':
                y = recession.area_wage['area_fips'[key]]
            if variable == 'qtrly_estabs_count':
                y = recession.area_firm['area_fips'[key]]
        if dimension == 'industry':
            if variable == 'month3_emplvl':
                y = recession.indus_empl['area_fips'[key]]
            if variable == 'avg_wkly_wage':
                y = recession.indus_wage['area_fips'[key]]
            if variable == 'qtrly_estabs_count':
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