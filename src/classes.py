from dictionaries import *
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt 
from urllib.request import urlopen
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
import matplotlib.ticker as mtick


class FipsLookup(FlaskForm):
    fips = StringField('area_fips', validators = [DataRequired(), Length(min=5, max =5)])
    

class Area(object):
    fips = StringField('Enter your fips code:', validators=[DataRequired(), Length(min=5, max =5)])
    submit = SubmitField('Search')

    def __init__(self, fips, df_2001, df_2008, df_2020):
        self.fips = fips
        self.title = area_dict[fips]
        self.recovery_2001 = df_2001['recovery'][self.fips] == 1
        self.growth_2001 = df_2001['delta'][self.fips]
        self.decline_2001 = df_2001['decline'][self.fips]
        self.nadir_2001 = df_2001['nadir'][self.fips]
        self.pre_peak_2001 = df_2001['pre_peak'][self.fips]
        self.post_peak_2001 = df_2001['post_peak'][self.fips]
        self.y_2001 = df_2001.loc[self.fips][1:33]
        self.fig_2001, self.ax_2001 = self.plot_2001()
        
        
        self.recovery_2008 = df_2008['recovery'][self.fips] == 1
        self.growth_2008 = df_2008['delta'][self.fips]
        self.decline_2008 = df_2008['decline'][self.fips]
        self.nadir_2008 = df_2008['nadir'][self.fips]
        self.pre_peak_2008 = df_2008['pre_peak'][self.fips]
        self.post_peak_2008 = df_2008['post_peak'][self.fips]
        self.y_2008 = df_2008.loc[self.fips][1:53]
        self.fig_2008, self.ax_2008 = self.plot_2008()

        self.forecast = round((df_2020['recov_likelihood'][self.fips]) *100, 2)
        self.jobs_2020 = '{:,.2f}'.format(df_2020['10'][self.fips])
        self.timeline_2001 = self.plot_2001()
        self.timeline_2008 = self.plot_2008()
        

    def plot_2001(self):
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize = (12,4))
        x = ['Q1 2000', 'Q2 2000', 'Q3 2000', 'Q4 2000', 'Q1 2001', 'Q2 2001', 'Q3 2001', 'Q4 2001',
         'Q1 2002', 'Q2 2002', 'Q3 2002', 'Q4 2002', 'Q1 2003', 'Q2 2003', 'Q3 2003', 'Q4 2003',
          'Q1 2004', 'Q2 2004', 'Q3 2004', 'Q4 2004', 'Q1 2005', 'Q2 2005', 'Q3 2005', 'Q4 2005',
           'Q1 2006', 'Q2 2006', 'Q3 2006', 'Q4 2006', 'Q1 2007', 'Q2 2007', 'Q3 2007', 'Q4 2007']
        y = self.y_2001
        ax.plot(x,y, color = 'green', linewidth = 1, alpha = 0.8)
        ax.axhline(y = self.nadir_2001, xmin = 'Q1 2000', xmax = 'Q4 2007', 
                    color = 'red', linewidth = .5, alpha = 0.5, label = 'nadir')
        ax.axhline(y = self.pre_peak_2001, xmin = 'Q1 2000', xmax = 'Q4 2007',
                    color = 'blue', linewidth = .5, alpha = .5, label = 'pre-recession-peak')
        ax.set_title('2001: ' + self.title)
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.axvline(x = 'Q3 2001', color = 'black', linewidth = 0.5, alpha = 0.5, label = '09/11/2001')
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('src/static/images/plot_2001.png')
        return fig, ax

    def plot_2008(self):
        sns.set_style('darkgrid')
        fig, ax = plt.subplots(figsize = (12,4))
        x = [   'Q1 2007', 'Q2 2007', 'Q3 2007', 'Q4 2007', 
                'Q1 2008', 'Q2 2008', 'Q3 2008', 'Q4 2008',
                'Q1 2009', 'Q2 2009', 'Q3 2009', 'Q4 2009',
                'Q1 2010', 'Q2 2010', 'Q3 2010', 'Q4 2010',
                'Q1 2011', 'Q2 2011', 'Q3 2011', 'Q4 2011',
                'Q1 2012', 'Q2 2012', 'Q3 2012', 'Q4 2012',
                'Q1 2013', 'Q2 2013', 'Q3 2013', 'Q4 2013',
                'Q1 2014', 'Q2 2014', 'Q3 2014', 'Q4 2014',
                'Q1 2015', 'Q2 2015', 'Q3 2015', 'Q4 2015',
                'Q1 2016', 'Q2 2016', 'Q3 2016', 'Q4 2016',
                'Q1 2017', 'Q2 2017', 'Q3 2017', 'Q4 2017',
                'Q1 2018', 'Q2 2018', 'Q3 2018', 'Q4 2018',
                'Q1 2019', 'Q2 2019', 'Q3 2019', 'Q4 2019']
        y = self.y_2008
        ax.plot(x,y, color = 'green', linewidth = 1, alpha = 0.8)
        ax.axhline(y = self.nadir_2008, xmin = 'Q1 2007', xmax = 'Q4 2019', 
                    color = 'red', linewidth = .5, alpha = 0.5, label = 'nadir')
        ax.axhline(y = self.pre_peak_2008, xmin = 'Q1 2007', xmax = 'Q4 2019',
                    color = 'blue', linewidth = .5, alpha = .5, label = 'pre-recession-peak')
        ax.set_title('2008: ' + self.title)
        ax.tick_params(axis='both', which='major', labelsize=10)
        ax.tick_params(axis='both', which='minor', labelsize=10)
        ax.ticklabel_format(style = 'plain', axis = 'y', scilimits = (9, -1)) 
        ax.get_yaxis().set_major_formatter(mtick.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.axvline(x = 'Q3 2008', color = 'black', linewidth = 0.5, alpha = 0.5, label = "'08 Financial Crisis")
        ax.legend(fancybox = True, borderaxespad=0)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('src/static/images/plot_2008.png')
        return fig, ax




