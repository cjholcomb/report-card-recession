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
    pre-peak : float
        high point of the timeline before the nadir. 
    nadir : float
        low point in the timeline. Excludes the first seven columns when computing.   
    post-peak : float
        high point of the timeline after the nadir.
    recovery : bool
        pre_peak <= post_peak
    delta : float
        difference between pre-peak and post-peak. 
    pre_peak_time : int
        number of quarters (from the beginning of the timeline) until the pre-peak.
    decline_time : int
        number of quarters between the pre-peak and the nadir.
    nadir_time : int
        number of quarters (from the beginning of the timeline) until the nadir.
    recovery_time : int, will be NaN if pre_peak < post_peak
        number of quarters between the andir and when the timeline surpasses the pre-peak. Will be NaN if recovery == 0.
    post_peak_time : int
        number of quarters (from the nadir) until the post-peak.
    growth_time : int, will be NaN if pre_peak < post_peak
        number of quarters between the recovery quarter and the post-peak
    pre_peak_qtr : str
        Highest quarter before the nadir
    nadir_qtr : str
        Lowest quarter of the timeline
    recovery_qtr : str, will be NaN if pre_peak < post_peak
        quarter after nadir at which the pre-peak is surpassed
    post_peak_qtr : str
        Highest quarter after the nadir
    
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
        
        loadpath = filepath(variable = variable, dimension = dimension, charttype= 'target', recession = self.recession.event_year, filetype = 'json')
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
        self.y = np.array(df.loc[key][1:self.recession.y_end], dtype=float)
        self.label = df[self.index_title].loc[key]
        
        self.pre_peak = df['pre_peak'].loc[key]
        self.nadir = df['nadir'].loc[key]
        self.recovery = df['recovery'].loc[key]
        self.post_peak = df['post_peak'].loc[key]
        self.delta = df['delta'].loc[key]

        self.pre_peak_time = df['pre_peak_time'].loc[key]
        self.decline_time = df['decline_time'].loc[key]
        self.nadir_time = df['nadir_time'].loc[key] 
        self.recovery_time = df['recovery_time'].loc[key]
        self.growth_time = df['growth_time'].loc[key]
        self.post_peak_time = df['post_peak_time'].loc[key]
        
        if self.recovery:
            self.recovery_qtr = quarters_display[df['recovery_qtr'].loc[key]]
        self.nadir_qtr = quarters_display[df['nadir_qtr'].loc[key]] 
        self.pre_peak_qtr = quarters_display[df['pre_peak_qtr'].loc[key]]
        self.post_peak_qtr = quarters_display[df['post_peak_qtr'].loc[key]]

    def plot_single(self, colorcode = True, check = False):
        """
        Plots the vector by itself.

        Parameters
        ----------
            colorcode : bool (default True)
                Determines if decline, recovery, and growth sections will be highlighted on the graph
            check : bool (default False)
                Determines if all important points will be charted. Used for troubleshooting.

        Returns
        -------
            fig : matplotlib plot
        """
        fig, ax = plt.subplots(figsize = (15, 4))
        x = self.recession.xaxis
        xi = np.arange(len(self.recession.xaxis))
        y = self.y
        y2 = self.pre_peak

        #plot the vector
        ax.plot(x, y, color = 'navy', linewidth = 2, alpha = 0.8, label = None)
        
        #plot the recession event
        ax.axvline(x = quarters_display[self.recession.event_quarter], color = 'black', linewidth = 1, alpha = .8, label = self.recession.event_label, linestyle = '--')
        ax.axhline(y = self.pre_peak, color = 'black', linewidth = 1, alpha = .8, label = 'Pre-peak: ' + self.pre_peak_qtr + ' (' + '{:,}'.format(self.pre_peak) +')', linestyle = '--')
        
        if check:
            ax.axvline(x = self.pre_peak_qtr, color = 'navy', linewidth = 1, alpha = .8, label = 'Pre-peak', linestyle = ':')
            ax.axvline(x = self.nadir_qtr, color = 'red', linewidth = 1, alpha = .8, label = 'Nadir', linestyle = ':')
            ax.axvline(x = self.post_peak_qtr, color = 'green', linewidth = 1, alpha = .8, label = 'Post-peak', linestyle = ':')
            ax.axhline(y = self.nadir, color = 'red', linewidth = 1, alpha = .8, linestyle = ':')
            ax.axhline(y = self.post_peak, color = 'green', linewidth = 1, alpha = .8, linestyle = ':')
            if self.recovery:
                ax.axvline(x = self.recovery_qtr, color = 'gold', linewidth = 1, alpha = .8, label = 'Recovery', linestyle = ':')

        if colorcode:
            pre_peak = x.index(self.pre_peak_qtr)
            nadir = x.index(self.nadir_qtr)
            
            #color the decline, recovery, and growth
            ax.fill_between(x=xi, y1=y, y2=y2, color='red', alpha=0.1, label='Decline', where=(xi >= pre_peak) & (xi <= nadir))
            if self.recovery:
                recovery = x.index(self.recovery_qtr)
                ax.fill_between(x=xi, y1=y, y2=y2, color='gold', alpha=0.1, label='Recovery', where=(xi >= nadir) & (xi <= recovery))
                ax.fill_between(x=xi, y1=y, y2=y2, color='green', alpha=0.1, label='Growth', interpolate = True, where=(xi >= recovery) & (y >= y2))
            else:
                ax.fill_between(x=xi, y1=y, y2=y2, color='gold', alpha=0.1, label='Recovery (incomplete)', where=(xi >= nadir))
            
        #define the title
        title = str(self.recession.event_year) + ' Recession: ' + self.label
        ax.set_title(title + ' (' + str(self.key) + ')')
        
        #set remaining chart properties and show
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        # ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        ax.set_ylabel(var_display[self.variable])
        plt.tight_layout()
        plt.show()
        return fig
        
    def plot_mulitple(self, keys, title = None, legend_outside = False):
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
        if legend_outside:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        else:
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

    def plot_siblings(self, legend_outside=False):
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
        return self.plot_mulitple(keys = keys, title = title, legend_outside = legend_outside)

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
    yabs_max = abs(max(ax.get_ylim(), key=abs))
    ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)
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
    yabs_max = abs(max(ax.get_ylim(), key=abs))
    ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)
    ax.set_xlabel('Quarters since start of recession')
    ax.set_ylabel('Growth')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_title(title)
    plt.legend()
    plt.show()
    return fig