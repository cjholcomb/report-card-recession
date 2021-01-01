import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np

from recessions import *
from areas import *
from industries import *

sns.set_style('darkgrid')





class Vector(object):
    """
    Stores critical information and creates charts for the report card.

    ...

    Attributes
    ----------
    key : int or str
        index of vector, unique identifier
    recession : int
        recession being charted
    dimension : str ('area' or 'industry')
        dimension being charted
    variable : str (month3_emplvl, avg_wkly_wage, or qrtly_estabs_count)
        variable/target being charted    
    df : pandas dataframe
        full timeline stored in a df
    event_quarter : float
        quarter in which the recession event takes place
    event_label : str
        read-friendly description of recession event
    index_col : int
        column that contains the unique identifier within the timeline
    index_title : int
        column that contains the reader-friendly industry/area title within the timeline
    x : list
        list of relevant quarters to use as an X-axis
    y : array-like
        datapoints to plot on the chart
    y_end : int
        number of columns to chart
    label : str
        reader-friendly title for the chart
    nadir : float
        low point in the timeline. Excludes the first seven columns when computing.</li>
    nadir_qtr : float
        number of quarters (from the beginning of the timeline) until the nadir.</li>
    pre-peak : float
        high point of the timeline before the nadir.
    pre_peak_qtr : int
        number of quarters (from the beginning of the timeline) until the pre-peak.</li>
    post-peak : float
        high point of the timeline after the nadir.
    post_peak_qtr : float
        number of quarters (from the nadir) until the post-peak.
    recovery : bool
        pre_peak <= post_peak
    recovery_qtr : float, will be NaN if pre_peak < post_peak
        number of quarters between the andir and when the timeline surpasses the pre-peak. Will be NaN if recovery == 0.
    decline : int
        number of quarters between the pre-peak and the nadir.
    delta : float
        difference between pre-peak and post-peak.
    
    Methods
    -------
    plot_single:
        Produces a timeline of a single vector with relevant areas shaded.
    plot_multiple:
        plots multiple vectora on the same chart
    plot_children:
        plots all child industries of a single industry
    plot_parent:
        plots the parent industry of a single industry
    plot_siblings:
        plots the sibling industries of a single industry. The given industry is included in the chart
    """

    def __init__ (self, key, recession = 2001, dimension ='area' , variable='month3_emplvl'):
        """
        Constructs the points needed to chart the vector.

        Parameters
        ----------
            key : str or int
                index of vector, unique identifier
            recession : int or 'full'
                recession timeline to compute.
            dimension : str 
                dimension of data to import. Must be 'area' or 'industry'. Default = 'area'.
            variable : str 
                determines what economic indicator will be used in the timeline. Must be one of ['month3_emplvl' (employment), 'avg_wkly_wage' (wages), 'qtrly_estabs_count'(firms)]
            
            
        """
        self.key = key
        self.recession = recession
        self.dimension = dimension
        self.variable = variable
        filepath =  "data/timelines_w_targets/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json" 
        self.y_end = end_columns[recession]
        df = pd.read_json(filepath)
        if dimension == 'industry':
            self.index_col = 'industry_code'
            self.index_title = 'industry_title'
        elif dimension == 'area':
            self.index_col = 'area_fips'
            self.index_title = 'area_title'
        df = df.set_index(self.index_col)
        self.df = df
        self.event_quarter = recession_events[recession]
        self.event_label = events_display[recession]
        recession = Recession(recession)
        self.x = recession.xaxis
        self.y = df.loc[key][1:self.y_end]
        self.label = df[self.index_title].loc[key]
        self.nadir = df['nadir'].loc[key]
        self.nadir_qtr = df['nadir_qtr'].loc[key] / 4 + recession.years[0]
        self.pre_peak = df['pre_peak'].loc[key]
        self.pre_peak_qtr = df['pre_peak_qtr'].loc[key] / 4 + recession.years[0]
        self.post_peak = df['post_peak'].loc[key]
        self.post_peak_qtr = df['post_peak_qtr'].loc[key] / 4 + recession.years[0]
        self.recovery = df['recovery'].loc[key]
        self.recovery_qtr = (df['nadir_qtr'].loc[key] + df['recovery_qtr'].loc[key]) / 4 + recession.years[0]
        self.decline = df['decline'].loc[key]
        self.delta = df['delta'].loc[key]

    def plot_single(self):
        fig, ax = plt.subplots(figsize = (15, 4))

        #plot the vector
        ax.plot(self.x,self.y, color = 'navy', linewidth = 2, alpha = 0.8, label = None)
        
        #plot the recession event
        ax.axvline(x = quarters_display[self.event_quarter], color = 'black', linewidth = 1, alpha = .8, label = self.event_label, linestyle = '--')
        
        #color the decline, recovery, and growth
        ax.fill_between(x = (quarters_display[self.pre_peak_qtr], quarters_display[self.nadir_qtr]), y1 = self.nadir, y2 = self.pre_peak, color = 'red', alpha = 0.1, label = 'Decline')
        if self.recovery:
            ax.fill_between(x = (quarters_display[self.nadir_qtr], quarters_display[self.recovery_qtr]), y1 = self.nadir, y2 = self.pre_peak, color = 'gold', alpha = 0.1, label = 'Recovery')
            ax.fill_between(x = (quarters_display[self.recovery_qtr], quarters_display[self.post_peak_qtr]), y1 = self.pre_peak, y2 = self.post_peak, color = 'green', alpha = 0.1, label = 'Growth')
        else:
            ax.fill_between(x = (quarters_display[self.nadir_qtr], self.x[-1]), y1 = self.nadir, y2 = self.pre_peak, color = 'gold', alpha = 0.1, label = 'Recovery (incomplete)')
        
        #define the title
        if self.variable == 'month3_emplvl':
            vartitle = ' Jobs: '
        elif self.variable == 'avg_wkly_wage':
            vartitle = ' Wages: '
        elif self.variable == 'qtrly_estabs_count':
            vartitle = ' Firms: '
        title = str(self.recession) + ' Recession' + vartitle + self.label
        ax.set_title(title + ' (' + str(self.key) + ')')
        
        #set remaining chart properties and show
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        #plot pre-peak, nadir, and recovery. Commented out for now
        ''' 
        ax.axhline(y = self.nadir, xmin = self.x[0], xmax = quarters_display[self.recovery_qtr], color = 'red', linewidth = .5,  alpha = 0.5, label = 'nadir: ' + str(quarters_display[self.nadir_qtr]))
        ax.axhline(y = self.pre_peak, xmin = self.x[0], xmax = quarters_display[self.recovery_qtr], color = 'blue', linewidth = .5, alpha = .5, label = 'pre-recession-peak: ' + str(quarters_display[self.pre_peak_qtr]), linestyle = '-')
        ax.axhline(y = self.post_peak, xmin = self.x[0], xmax = self.x[-1], color = 'blue', linewidth = .5, alpha = .5, label = 'post-recession-peak: ' + str(quarters_display[self.post_peak_qtr]))
        ax.axvline(x = quarters_display[self.recovery_qtr], color = 'purple', linewidth = 0.5, alpha = 0.5, label = 'recovery: ' + str(quarters_display[self.recovery_qtr]), linestyle =':')
        '''
        
    def plot_mulitple(self, keys, title = None):
        df = self.df
        fig, ax = plt.subplots(figsize = (15, 4))
        for key in keys:
            y = df.loc[key][1:self.y_end]
            label = str(key) + ": " + df[self.index_title].loc[key]
            ax.plot(self.y, linewidth = 1, alpha = 0.8, label = label)
        if title:
            ax.set_title(title + ' (' + str(self.key) + ')')
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_children(self):
        if self.dimension != 'industry':
            pass
        industry = Industry(self.key)
        title = 'Child industries of ' +  str(self.key) +  self.label
        keys = industry.children
        self.plot_mulitple(keys = keys, title = title)

    def plot_parent(self):
        if self.dimension != 'industry':
            pass
        industry = Industry(self.key)
        title = str(industry.code) + ": " +  industry.title
        keys = [industry.parent]
        self.plot_mulitple(keys = keys, title = title)

    def plot_siblings(self):
        if self.dimension != 'industry':
            pass
        industry = Industry(self.key)
        title = 'Child industries of ' +  str(self.key) +  self.label
        keys = industry.siblings
        self.plot_mulitple(keys = keys, title = title)

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