import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np

from produce_datasets import filepath

from recessions import *
from areas import *
from industries import *

var_display ={'month3_emplvl': 'Total Employment', 'avg_wkly_wage': 'Avg. Weekly Wages', 'qtrly_estabs_count':'# of Establishments/Firms'}

sns.set_style('darkgrid')

class Vector(object):
    """
    Stores critical information and creates charts for the report card.

    ...

    Attributes
    ----------
    key : int or str
        index of vector, unique identifier
    recession : object
        Recession class object (recessions.py)
    dimension : str ('area' or 'industry')
        dimension being charted
    variable : str (month3_emplvl, avg_wkly_wage, or qrtly_estabs_count)
        variable/target being charted    
    index_col : int
        column that contains the unique identifier within the timeline
    index_title : int
        column that contains the reader-friendly industry/area title within the timeline
    row : object (Industry or Area)
        class object to pull additional attributes.
    df : pandas dataframe
        full timeline stored in a df 
    y : array-like
        datapoints to plot on the chart 
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
        plots multiple vectors on the same chart
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
        Some attributes will be Recession, Industry, or Area class objects.

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
        self.recession = Recession(recession)
        self.dimension = dimension
        self.variable = variable
        loadpath = filepath(recession = recession, dimension = dimension , variable = variable, charttype = 'target')
        # filepath =  "data/timelines_w_targets/" + dim_abbr[dimension] + "_" + var_abbr[variable] + "_" + str(recession) + ".json" 
        # self.y_end = end_columns[recession]
        df = pd.read_json(loadpath)
        if dimension == 'industry':
            self.index_col = 'industry_code'
            self.index_title = 'industry_title'
            self.row = Industry(key)
        elif dimension == 'area':
            self.index_col = 'area_fips'
            self.index_title = 'area_title'
            self.row = Area(key)
        df = df.set_index(self.index_col)
        self.df = df
        # self.event_quarter = recession_events[recession]
        # self.event_label = events_display[recession]
        # self.x = self.recession.xaxis
        self.y = df.loc[key][1:self.recession.y_end]
        self.label = df[self.index_title].loc[key]
        self.nadir = df['nadir'].loc[key]
        self.nadir_qtr = df['nadir_qtr'].loc[key] / 4 + self.recession.years[0]
        self.pre_peak = df['pre_peak'].loc[key]
        self.pre_peak_qtr = df['pre_peak_qtr'].loc[key] / 4 + self.recession.years[0]
        self.post_peak = df['post_peak'].loc[key]
        self.post_peak_qtr = df['post_peak_qtr'].loc[key] / 4 + self.recession.years[0]
        self.recovery = df['recovery'].loc[key]
        self.recovery_qtr = (df['nadir_qtr'].loc[key] + df['recovery_qtr'].loc[key]) / 4 + self.recession.years[0]
        self.decline = df['decline'].loc[key]
        self.delta = df['delta'].loc[key]

    def plot_single(self, colorcode = True):
        """
        Plots the vector by itself.

        Parameters
        ----------
            colorcode : bool
                Determines if decline, recovery, and growth sections will be highlighted on the graph

        Returns
        -------
            fig : matplotlib plot
        """
        fig, ax = plt.subplots(figsize = (15, 4))

        #plot the vector
        ax.plot(self.recession.xaxis, self.y, color = 'navy', linewidth = 2, alpha = 0.8, label = None)
        
        #plot the recession event
        ax.axvline(x = quarters_display[self.recession.event_quarter], color = 'black', linewidth = 1, alpha = .8, label = self.recession.event_label, linestyle = '--')
        
        if colorcode:
            #color the decline, recovery, and growth
            ax.fill_between(x = (quarters_display[self.pre_peak_qtr], quarters_display[self.nadir_qtr]), y1 = self.nadir, y2 = self.pre_peak, color = 'red', alpha = 0.1, label = 'Decline')
            # ax.fill_between(x = (quarters_display[self.pre_peak_qtr], quarters_display[self.nadir_qtr]), y1 = self.nadir, y2 = self.pre_peak, color = 'red', alpha = 0.1, label = 'Decline')
            if self.recovery:
                ax.fill_between(x = (quarters_display[self.nadir_qtr], quarters_display[self.recovery_qtr]), y1 = self.nadir, y2 = self.pre_peak, color = 'gold', alpha = 0.1, label = 'Recovery')
                ax.fill_between(x = (quarters_display[self.recovery_qtr], quarters_display[self.post_peak_qtr]), y1 = self.pre_peak, y2 = self.post_peak, color = 'green', alpha = 0.1, label = 'Growth')
            else:
                ax.fill_between(x = (quarters_display[self.nadir_qtr], self.recession.xaxis[-1]), y1 = self.nadir, y2 = self.pre_peak, color = 'gold', alpha = 0.1, label = 'Recovery (incomplete)')
            
        #define the title
        title = str(self.recession.event_year) + ' Recession: ' + self.label
        ax.set_title(title + ' (' + str(self.key) + ')')
        
        #set remaining chart properties and show
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        ax.set_ylabel(var_display[self.variable])
        plt.tight_layout()
        plt.show()
        return fig

        #plot pre-peak, nadir, and recovery. Commented out for now
        ''' 
        ax.axhline(y = self.nadir, xmin = self.x[0], xmax = quarters_display[self.recovery_qtr], color = 'red', linewidth = .5,  alpha = 0.5, label = 'nadir: ' + str(quarters_display[self.nadir_qtr]))
        ax.axhline(y = self.pre_peak, xmin = self.x[0], xmax = quarters_display[self.recovery_qtr], color = 'blue', linewidth = .5, alpha = .5, label = 'pre-recession-peak: ' + str(quarters_display[self.pre_peak_qtr]), linestyle = '-')
        ax.axhline(y = self.post_peak, xmin = self.x[0], xmax = self.x[-1], color = 'blue', linewidth = .5, alpha = .5, label = 'post-recession-peak: ' + str(quarters_display[self.post_peak_qtr]))
        ax.axvline(x = quarters_display[self.recovery_qtr], color = 'purple', linewidth = 0.5, alpha = 0.5, label = 'recovery: ' + str(quarters_display[self.recovery_qtr]), linestyle =':')
        '''
        
    def plot_mulitple(self, keys, title = None):
        """
        Plots a series of lines.

        Parameters
        ----------
            keys : list or list-like
                list of indicies to be plotted on the chart.
            title : str, default None
                overwrites automatic assignment of chart title.

        Returns
        -------
            fig : matplotlib plot
        """
        df = self.df
        fig, ax = plt.subplots(figsize = (15, 4))
        for key in keys:
            y = df.loc[key][1:self.recession.y_end]
            label = str(key) + ": " + df[self.index_title].loc[key]
            ax.plot(self.recession.xaxis, y, linewidth = 1, alpha = 0.8, label = label)
        if title:
            ax.set_title(title)
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend(fancybox = True, borderaxespad=0)
        ax.set_ylabel(var_display[self.variable])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def plot_children(self):
        """
        Plots all child industries of the vector

        Parameters
        ----------
            None

        Returns
        -------
            fig : matplotlib plot
        """
        if self.dimension != 'industry':
            pass
        title = 'Child industries of: ' + self.row.title + " (" + str(self.key) + ")" 
        keys = self.row.children
        return self.plot_mulitple(keys = keys, title = title)

    def plot_parent(self, title = None):
        """
        Plots the parent industry of the vector

        Parameters
        ----------
            title : str, default None
                overwrites automatic assignment of chart title.

        Returns
        -------
            fig : matplotlib plot
        """
        if self.dimension != 'industry':
            pass
        keys = [self.row.parent]
        title = 'Parent industry of: ' + self.row.title + " (" + str(self.key) + ")" 
        return self.plot_mulitple(keys = keys, title = title)

    def plot_siblings(self):
        """
        Plots all sibling industries of the vector, including the vector itself.

        Parameters
        ----------
            None

        Returns
        -------
            fig : matplotlib plot
        """
        if self.dimension != 'industry':
            pass
        title = 'Sibling industries of: ' + self.row.title + " (" + str(self.key) + ")"
        keys = self.row.siblings
        return self.plot_mulitple(keys = keys, title = title)

def recession_comparison(key, variable, dimension):
    '''
    Creates the "scary chart"- proportional growth for a single area/industry. All recessions included in chart.

        Parameters: 
            key (str or int): area-fips or industry_code
            variable (str): determines what economic indicator will be used in the timeline. Must be one of ['month3_emplvl' (employment), 'avg_wkly_wage' (wages), 'qtrly_estabs_count'(firms)]
            dimension (str): dimension of data to chart.
            
        Returns: 
            fig (matplotlib plot)
    '''
    fig, ax = plt.subplots(figsize =(15, 10))
    if dimension == 'area':
        index = 'area_fips'
        title = 'Recession Comparison, ' + area_titles[key] + " (" + str(key) + ")" 
    elif dimension == 'industry':
        index = 'industry_code'
        title = 'Recession Comparison: ' + industry_titles[key] + " (" + str(key) + ")" 
    for recession in recessions_int.keys():
        if recession == 'full':
            break
        loadpath = filepath(variable = variable, dimension = dimension, charttype = 'proportional', recession = recession, filetype = 'json')
        df = pd.read_json(loadpath)
        df.set_index(index, inplace = True)
        ax.plot(df.loc[key][1:-1]*100, label = str(recession), linewidth = 1.5, alpha = 0.8)
    ax.axvline(x = 6, color = 'black', linewidth = 0.8, alpha = 0.5, ls = ':', label = 'Event Quarter')
    ax.axhline(y = 0, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '--', label = 'Pre-Recession baseline')
    ax.set_xlabel('Quarters since start of recession')
    ax.set_ylabel('Growth: ' + var_display[variable])
    ax.set_title(title)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.legend()
    plt.show()
    return fig

def variable_comparison(key, recession, dimension):
    '''
    Creates the "scary chart"- proportional growth for a single area/industry. All recessions included in chart.

        Parameters: 
            key (str or int): area-fips or industry_code
            recession (int): determines which recession timeline to chart. 'full' will cause function to exit.
            dimension (str): dimension of data to chart.
            
        Returns: 
            fig (matplotlib plot)
    '''
    if recession == 'full':
        pass
    fig, ax = plt.subplots(figsize =(15, 10))
    if dimension == 'area':
        index = 'area_fips'
        title = area_titles[key] + ' (' + str(key) + ') ' + 'performance: ' + str(recession) + ' recession'
    elif dimension == 'industry':
        index = 'industry_code'
        title = industry_titles[key] + ' (' + str(key) + ') ' + 'performance: ' + str(recession) + ' recession'
    for variable in var_abbr.keys():
        if recession == 'full':
            break
        loadpath = filepath(variable = variable, dimension = dimension, charttype = 'proportional', recession = recession, filetype = 'json')
        df = pd.read_json(loadpath)
        df.set_index(index, inplace = True)
        ax.plot((df.loc[key][1:-1])*100, label = var_display[variable], linewidth = 1.5, alpha = 0.8)
    ax.axvline(x = 6, color = 'black', linewidth = 0.8, alpha = 0.5, ls = ':', label =  events_display[recession],)
    ax.axhline(y = 0, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '--', label = 'Pre-Recession baseline')
    ax.set_xlabel('Quarters since start of recession')
    ax.set_ylabel('Growth')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_title(title)
    plt.legend()
    plt.show()
    return fig