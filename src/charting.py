import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick
import seaborn as sns
import pandas as pd
import numpy as np

from constants import *
from classes import *

sns.set_style('darkgrid')

#establishes linestyle and color consistency  
styling = {2001:'navy', 2008: 'maroon', 2020:'green', 'empl': '-', 'wage':'--', 'firm':':'}

def plot_timelines(keys, emphasize = None, recession = 2008, variable = 'empl',title = None, legend_outside = False, show = True, savepath = None):
    """
    Plots several timelines.
    
    Parameters: 
        keys (list of str or int): area-fips or industry_codes to chart. 
        emphasize (int or str): area-fips or industry_code to emphasize in charting.
        recession (int): determines which recession timeline to chart. 'full' will cause function to exit. 
        variable (str): determines what economic indicator will be used in the timeline.
        title (str): Optional. Title of chart
        legend_outside (bool): Moves the legend outside the plot (if it covers data). Default False.
        show (bool): Determines if the chart will be shown. Default True.    
        savepath (str): determines if the chart will be saved locally.

    Returns: 
        matplotlib axis
    """
    
    if type(recession) == str:
        pass
    
    recession = Recession(recession)
    
    if all(isinstance(x, str) for x in keys):
        dimension = 'area'
        index = 'area_fips'
    else: 
        dimension = 'industry'
        index = 'industry_code' 
    
    loadpath = filepath(variable = variable, dimension = dimension, charttype= 'target', recession = recession.event_year, filetype = 'json')
    df = pd.read_json(loadpath)
    df.set_index(index, inplace = True)
    
    fig, ax = plt.subplots(figsize = (15, 4))
    for key in keys:
        # vector = Vector(key, recession = recession, variable= variable)
        y = df.loc[key][1:END_COLUMNS[recession.event_year]]
        # y = vector.y
        label = str(key) + ": " + df['industry_title'].loc[key]
        if key == emphasize:
            ax.plot(recession.xaxis, y, linewidth = 1.5, alpha = 1, color = 'black', ls = '--')
        else:
            ax.plot(recession.xaxis, y, linewidth = 1, alpha = 0.8, label = label, ls = '-')
    if title:
        ax.set_title(title)
    ax.tick_params(axis='both', which='major', labelsize=10)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
    ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.legend(fancybox = True, borderaxespad=0)
    ax.set_ylabel(VARNAME_LABEL[variable])
    if show:
        plt.xticks(rotation=45)
        if legend_outside:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    if savepath:
        plt.xticks(rotation=45)
        if legend_outside:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(savepath)
    return fig    

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

    def __init__ (self, key, recession = 2001, variable='empl'):
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
                determines what economic indicator will be used in the timeline.      
        """
        
        self.key = key
        self.recession = Recession(recession)
        if type(key) == str:
            self.dimension = 'area'
        elif type(key) == int:
            self.dimension = 'industry'
        self.variable = variable
        
        loadpath = filepath(variable = variable, dimension = self.dimension, charttype= 'target', recession = self.recession.event_year, filetype = 'json')
        df = pd.read_json(loadpath)
        if self.dimension == 'industry':
            self.index_col = 'industry_code'
            self.index_title = 'industry_title'
            self.row = Industry(key)
        elif self.dimension == 'area':
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
            self.recovery_qtr = QUARTERS[df['recovery_qtr'].loc[key]]
        else:
            self.recovery_qtr = None
        self.nadir_qtr = QUARTERS[df['nadir_qtr'].loc[key]] 
        self.pre_peak_qtr = QUARTERS[df['pre_peak_qtr'].loc[key]]
        self.post_peak_qtr = QUARTERS[df['post_peak_qtr'].loc[key]]

        pcg = '{:.2%}'
        self.decline_pcg = pcg.format((self.pre_peak - self.nadir) / self.pre_peak) 
        self.growth_pcg = pcg.format(self.delta / self.pre_peak)


    def plot_self(self, colorcode = True, check = False, show = True, savepath = None, title = None):
        '''
        Plots a single vector (one recession, one target/variable, one area/industry)
    
        Parameters
        ----------
            colorcode : bool
                Determines if decline, recovery, and growth sections will be highlighted on the graph. Default True.
            check : bool
                Determines if all important points will be charted. Used for troubleshooting. Default False
            show : bool
                Determines if the chart will be shown. Default True.    
            savepath : str 
                location to save image file. Will not save if None. 
            title : str
                overrides generated chart title

        Returns
        -------
            matplotlib axis
        '''
        
        fig, ax = plt.subplots(figsize = (15, 4))
    
        #define critical variables
        x = self.recession.xaxis
        xi = np.arange(len(self.recession.xaxis))
        y = self.y
        y2 = self.pre_peak

        #plot the vector
        ax.plot(x, y, color = styling[self.recession.event_year], linewidth = 2, alpha = 0.8, label = None, ls = styling[self.variable])
        
        #plot the recession event
        ax.axvline(x = QUARTERS[self.recession.event_quarter], color = 'black', linewidth = 1, alpha = .8, label = self.recession.event_label, linestyle = '-.')
        
        #plot the pre-peak line
        ax.axhline(y = self.pre_peak, color = 'black', linewidth = 1, alpha = .8, label = 'Pre-peak: ' + self.pre_peak_qtr + ' (' + '{:,}'.format(self.pre_peak) +')', linestyle = '-.')
        
        #show lines for troubleshooting
        if check:
            ax.axvline(x = self.pre_peak_qtr, color = 'navy', linewidth = 1, alpha = .8, label = 'Pre-peak', linestyle = ':')
            ax.axvline(x = self.nadir_qtr, color = 'red', linewidth = 1, alpha = .8, label = 'Nadir', linestyle = ':')
            ax.axvline(x = self.post_peak_qtr, color = 'green', linewidth = 1, alpha = .8, label = 'Post-peak', linestyle = ':')
            ax.axhline(y = self.nadir, color = 'red', linewidth = 1, alpha = .8, linestyle = ':')
            ax.axhline(y = self.post_peak, color = 'green', linewidth = 1, alpha = .8, linestyle = ':')
            if self.recovery:
                ax.axvline(x = self.recovery_qtr, color = 'gold', linewidth = 1, alpha = .8, label = 'Recovery', linestyle = ':')

        #show shading
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
        if title:
            ax.set_title(title)
        else:
            title = str(self.recession.event_year) + ' Recession: ' + self.label
            ax.set_title(title + ' (' + str(self.key) + ')')
        
        #set remaining chart properties
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend(fancybox = True, borderaxespad=0)
        ax.set_ylabel(VARNAME_LABEL[self.variable])
        
        #show the chart
        if show:
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

        #save the chart
        if savepath:
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(savepath)
        return ax
 
    def plot_children(self, legend_outside = False, show = True, savepath = None, title = None):
        """
        Plots all child industries of the vector

        Parameters
        ----------
            legend_outside : bool
                moves the legend outside the plot (if it covers data). Default False.
            show : bool 
                determines if the chart will be shown. Default True.    
            savepath : str 
                determines if the chart will be saved locally.
            title : str
                overrides generated title

        Returns
        -------
            matplotlib axis
        """
        if self.dimension != 'industry':
            pass
        if not title:
            title = 'Child industries of: ' + self.row.title + " (" + str(self.key) + ")" 
        ax = plot_timelines(keys = self.row.children, recession = self.recession.event_year, variable = self.variable, title = title, legend_outside = legend_outside, show = show, savepath = savepath)
        return ax

    def plot_parent(self, show = True, savepath = None, title = None, legend_outside = False):
        """
        Plots the parent industry of the vector

        Parameters
        ----------
            show : bool
                Determines if the chart will be shown. Default True.    
            savepath : str 
                determines if the chart will be saved locally.
            title : str
                overrides generated title
            legend_outside : bool
                Moves the legend outside the plot. Default False.

        Returns
        -------
            fig : matplotlib plot
        """
        if self.dimension != 'industry':
            pass
        if not title:
            title = 'Parent industry of: ' + self.row.title + " (" + str(self.key) + ")" 
        return plot_timelines(keys = [self.row.parent], recession= self.recession.event_year, title = title, show = show, savepath = savepath, legend_outside = legend_outside)

    def plot_siblings(self, legend_outside = False, show = True, savepath = None, title = None):
        """
        Plots all sibling industries of the vector, including the vector itself.

        Parameters
        ----------
            legend_outside : bool
                moves the legend outside the plot (if it covers data). Default False.
            show : bool 
                determines if the chart will be shown. Default True.    
            savepath : str 
                determines if the chart will be saved locally.
            title : str
                overrides generated title

        Returns
        -------
            fig : matplotlib plot
        """
        if self.dimension != 'industry':
            pass
        if not title:
            title = 'Sibling industries of: ' + self.row.title + " (" + str(self.key) + ")"
        ax = plot_timelines(keys = self.row.siblings, emphasize = self.key, recession = self.recession.event_year, variable = self.variable, title = title, legend_outside = legend_outside, show = show, savepath = savepath)
        return ax

def recession_comparison(key, variable = 'empl', show = True, savepath = None):
    '''
    Creates the "scary chart"- proportional growth for a single area/industry. All recessions included in chart.

        Parameters: 
            key (str or int): area-fips or industry_code
            variable (str): determines what economic indicator will be used in the timeline. 
            show (bool): determines if the chart will be shown to the user. Default True.
            savepath (str): determines if the chart will be saved locally. 

        Returns: 
            matplotlib plot
    '''
    fig, ax = plt.subplots(figsize =(15, 5))
    if type(key) == str:
        dimension = 'area'
        index = 'area_fips'
    else: 
        dimension = 'industry'
        index = 'industry_code'  
    title = 'Recession Comparison, ' + VARNAME_LABEL[variable]+ ': ' + TITLE[key] + " (" + str(key) + ")" 
    for recession in VALID_RECESSIONS:
        loadpath = filepath(variable = variable, dimension = dimension, charttype = 'proportional', recession = recession, filetype = 'json')
        df = pd.read_json(loadpath)
        df.set_index(index, inplace = True)
        ax.plot(df.loc[key][1:-1]*100, label = str(recession), linewidth = 1.5, alpha = 0.8, color = styling[recession], ls = styling[variable])
    ax.axvline(x = 6, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '-.', label = 'Event Quarter')
    ax.axhline(y = 0, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '-.', label = 'Pre-Recession baseline')
    yabs_max = abs(max(ax.get_ylim(), key=abs))
    ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)
    ax.set_xlabel('Quarters since start of recession')
    ax.set_ylabel('Growth: ' + VARNAME_LABEL[variable])
    ax.set_title(title)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend()
    if savepath:
        plt.savefig(savepath)
    if show:
        plt.show()
    return fig

def variable_comparison(key, recession, show = True, savepath = None):
    '''
    Creates the "scary chart"- proportional growth for a single area/industry. All variables included in chart.

        Parameters: 
            key (str or int): area-fips or industry_code
            recession (int): determines which recession timeline to chart. 'full' will cause function to exit.
            show (bool): determines if the chart will be shown to the user. Default True.
            savepath (str): determines if the chart will be saved locally.

        Returns: 
            matplotlib plot
    '''
    if recession == 'full':
        pass
    fig, ax = plt.subplots(figsize =(15, 5))
    if type(key) == str:
        dimension = 'area'
        index = 'area_fips'
    else: 
        dimension = 'industry'
        index = 'industry_code'  
    title = str(recession) + ' Recession: ' + TITLE[key] + " (" + str(key) + ")" 
    for variable in VARNAME_LONG.keys():
        if recession == 'full':
            break
        loadpath = filepath(variable = variable, dimension = dimension, charttype = 'proportional', recession = recession, filetype = 'json')
        df = pd.read_json(loadpath)
        df.set_index(index, inplace = True)
        ax.plot((df.loc[key][1:-1])*100, label = VARNAME_LABEL[variable], linewidth = 1.5, alpha = 0.8, color = styling[recession], ls = styling[variable])
    ax.axvline(x = 6, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '-.', label =  EVENT[recession])
    ax.axhline(y = 0, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '-.', label = 'Pre-Recession baseline')
    yabs_max = abs(max(ax.get_ylim(), key=abs))
    ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)
    ax.set_xlabel('Quarters since start of recession')
    ax.set_ylabel('Growth')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.set_title(title)
    ax.legend()
    if savepath:
        print(savepath)
        fig.savefig(savepath)
    if show:
        plt.show()
    return fig

def full_comparison(key, show = True, savepath = None):
    '''
    Creates the "scary chart"-Includes all targets/variables (stratified by linestyle) and recessions (startified by color)

        Parameters: 
            key (str or int): area-fips or industry_code
        show (bool): determines if the chart will be shown to the user. Default True.
        savepath (str): determines if the chart will be saved locally.

        Returns: 
            matplotlib plot
    '''
    fig, ax = plt.subplots(figsize =(15, 5))
    if type(key) == str:
        dimension = 'area'
        index = 'area_fips'
    else: 
        dimension = 'industry'
        index = 'industry_code' 
    title = 'Recession Comparison, ' + TITLE[key] + " (" + str(key) + ")" 
    for recession in VALID_RECESSIONS:
        for variable in VARNAME_LONG.keys(): 
            loadpath = filepath(variable = variable, dimension = dimension, charttype = 'proportional', recession = recession, filetype = 'json')
            df = pd.read_json(loadpath)
            df.set_index(index, inplace = True)
            ax.plot(df.loc[key][1:-1]*100, label = str(recession), linewidth = 1.5, alpha = 0.8, color = styling[recession], ls = styling[variable])
    ax.axvline(x = 6, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '-.', label = 'Event Quarter')
    ax.axhline(y = 0, color = 'black', linewidth = 0.8, alpha = 0.5, ls = '-.', label = 'Pre-Recession baseline')
    yabs_max = abs(max(ax.get_ylim(), key=abs))
    ax.set_ylim(ymin=-yabs_max, ymax=yabs_max)
    ax.set_xlabel('Quarters since start of recession')
    ax.set_ylabel('Growth: ' + VARNAME_LABEL[variable])
    ax.set_title(title)
    ax.yaxis.set_major_formatter(mtick.PercentFormatter())
    ax.legend()
    if savepath:
        plt.savefig(savepath)
    if show:
        plt.show()
    return fig

def produce_stats(key):
    commas = "{:,}"
    pcg = '{:.2%}'
    dollars = "${:,.2f}"
    stats ={}
    for recession in VALID_RECESSIONS:
        stats[recession] = {}
        for variable in VARNAME_LONG.keys():
            stats[recession][variable] ={}
            
            vector = Vector(key, recession, variable)
            stats[recession][variable]['recovery'] = vector.recovery

            #Numeric Stats
            if variable == 'wage':
                stats[recession][variable]['pre_peak'] = dollars.format(int(vector.pre_peak))
                stats[recession][variable]['nadir'] = dollars.format(int(vector.nadir))
                stats[recession][variable]['post_peak'] = dollars.format(int(vector.post_peak))
                stats[recession][variable]['delta'] = dollars.format(int(vector.delta))
            else:
                stats[recession][variable]['pre_peak'] = commas.format(int(vector.pre_peak))
                stats[recession][variable]['nadir'] = commas.format(int(vector.nadir))
                stats[recession][variable]['post_peak'] = commas.format(int(vector.post_peak))
                stats[recession][variable]['delta'] = commas.format(int(vector.delta))

            #Time Stats
            stats[recession][variable]['decline_time'] = str(vector.decline_time / 4) + ' years'
            if vector.recovery:
                stats[recession][variable]['recovery_time'] = str((vector.recovery_time + vector.decline_time)/ 4) + ' years'
                stats[recession][variable]['growth_time'] = str(vector.growth_time / 4) + ' years'
            else:
                stats[recession][variable]['recovery_time'] = None
                stats[recession][variable]['growth_time'] = None

            #Quarter Markers Stats
            stats[recession][variable]['pre_peak_qtr'] = vector.pre_peak_qtr
            stats[recession][variable]['nadir_qtr'] = vector.nadir_qtr
            stats[recession][variable]['recovery_qtr'] = vector.recovery_qtr
            stats[recession][variable]['post_peak_qtr'] = vector.post_peak_qtr

            #Percentage Stats
            stats[recession][variable]['decline_pcg'] = vector.decline_pcg 
            stats[recession][variable]['growth_pcg'] = vector.growth_pcg
    return stats

def subjective_charts(key):
    full_comparison(key = key, show = False, savepath = 'src/static/images/compfull.png')
    for recession in VALID_RECESSIONS:
        savepath = 'src/static/images/compvar_' + str(recession) + '.png'
        variable_comparison(key = key, recession = recession, show = False, savepath = savepath)
    for variable in VARNAME_LONG.keys():
        savepath = 'src/static/images/comprec_' + str(variable) + '.png'
        recession_comparison(key = key, variable = variable, show = False, savepath = savepath)
    recession_comparison(key = key, variable = 'wage', show = False, savepath = 'src/static/images/comprec_wage.png') 
    recession_comparison(key = key, variable = 'firm', show = False, savepath = 'src/static/images/comprec_firm.png') 

def objective_charts(key):
    for recession in VALID_RECESSIONS:
        for variable in VARNAME_LONG.keys():
            vector = Vector(key, recession, variable)
            savepath = 'src/static/images/' + variable + '_' + str(recession) + '.png'
            vector.plot_self(colorcode = True, check = False, show = False, savepath = savepath)