import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np
import pandas as pd  

from constants import *
# from charting import plot_single, plot_multiple

class Recession(object):
    """
    Stores relevant information for each recession.

    ...

    Attributes
    ----------
    years : list
        years included in recession analysis. Must be numeric
    event_year : int
        year in which recession event takes place
    event_quarter : float
        quarter in which recession event takes place
    event_label : str
        read-friendly description of recession event
    quarters : list
        list of quarters included in recession analysis
    xaxis : list
        list of reader-friendly quarters in recession analys
         


    Methods
    -------
    derive_generation:
        Computes the industry's generation
    """

    def __init__(self, year = 2008):
        """
        Constructs necessary attributes for the recession

        Parameters
        ----------
            year : int (or 'full')
                year of recession, used as unique identifier
        """
        self.years = RECESSION_YEARS[year]
        self.event_year = year
        if year != 'full':
            self.event_quarter = EVENT_QUARTER[int(year)]
            self.event_label = EVENT[int(year)]
        self.quarters = [quarter for quarter in QUARTERS.keys() if quarter > min(self.years) and quarter <= (max(self.years) + 1)]
        self.xaxis = [v for k,v in QUARTERS.items() if k in self.quarters]
        self.y_end = END_COLUMNS[year]

class Area(object):
    """
    Stores critical information for a given area to facilitate reporting.

    ...

    Attributes
    ----------
    index : str
        index variable/unique identifier. Must be 5 digits.
    title : str
        Reader-friendly display text for the area. 
    type : str
        type of area in question (County, City, State, etc.)
    state: st
        two-letter postal desgination of the area's state. Currently not implemented for CSAs or MSAs. Includes PR and VI.

    Methods
    -------
    None
    """

    def __init__(self, fips):
        """
        Constructs the necessary attributes.

        Parameters
        ----------
            fips : str
                area-fips code (unique identifer) of the area.
        """

        self.index = fips
        self.title = TITLE[fips]
        if fips.startswith('US'):
            self.type = 'Nationwide'
            self.state = 'US'
        elif fips in STATE_ABBR.keys():
            self.type = 'State'
            self.state = STATE_ABBR[fips]
        elif fips.startswith('CS'):
            self.type = 'Combined Statsitical Area'
            self.state = None
        elif fips.startswith('C'):
            self.type = 'Metropolitan Statistical Area'
            self.state = None
        elif STATE[fips] == '72000':
            self.type = 'Municipio'
            self.state = STATE_ABBR[STATE[fips]]
        elif STATE[fips] == '78000':
            self.type = 'Island'
            self.state = STATE_ABBR[STATE[fips]]
        else:
            self.type = 'County'
            self.state = STATE_ABBR[STATE[fips]]

class Industry(object):
    """
    Stores relevant information for each industry.

    ...

    Attributes
    ----------
    index : int
        index variable/unique identifier.
    title : str
        Reader-friendly display text for the industry.
    generation : int
        where in the hierarchy the industry falls. High numbers = lower in this hierarchy
    parent : int
        code of industry above in the hierarchy
    children : list
        codes of industries directly below in the hierarchy
    siblings : list
        codes of industries that share a parent industry
    orphan : bool
        indicates if industry is idnentical to parent (no siblings)

    Methods
    -------
    derive_generation:
        Computes the industry's generation
    """
    def __init__(self, code):
        """
        Constructs necessary attributes for the industry

        Parameters
        ----------
            code : int
                numeric unique identifer of the industry.
        """
        self.index = code
        self.title = TITLE[code]
        self.generation = self.derive_generation(code)
        if code == 10:
            self.parent = None
        else:
            self.parent = PARENT[code]
        if self.generation == 7:
            self.children = []
        else:
            self.children = CHILD[code]
        
        if code == 10:
            self.siblings = [10]
            self.orphan = True
        else:
            self.siblings = SIBLINGS[code]
            self.orphan = len(self.siblings) == 1
                
    def derive_generation(self, code):
        """
        Computes the industry's generation

        Parameters
        ----------
            code : int
                numeric unique identifer of the industry.

        Returns
        -------
            generation : int
                industry generation identifier
        """
        if code == 10:
            return 0
        elif code <= 99:
            return 3
        elif code <= 102:
            return 1
        elif code <= 999:
            return 4
        elif code <= 1029:
            return 2
        elif code <= 9999:
            return 5
        elif code <= 99999:
            return 6
        elif code <= 999999:
            return 7 

    # def recession_stats():
    #     self.2001

   # def chart_profile(self, dimension = 'industry', compvar = False, comprec = True, single = False):
        
    #     if compvar:
    #         self.compvar_2001 = variable_comparison(key = self.index, recession= 2001, dimension= 'industry', show = False, savepath = None)
    #         self.compvar_2008 = variable_comparison(key = self.index, recession= 2008, dimension= 'industry', show = False, savepath = None)
        
    #     if comprec:
    #         self.comprec_empl = recession_comparison(key = self.index, variable = 'month3_emplvl', dimension= 'industry', show = False, savepath = None)
    #         self.comprec_wage = recession_comparison(key = self.index, variable = 'avg_wkly_wage', dimension= 'industry', show = False, savepath = None)
    #         self.comprec_wage = recession_comparison(key = self.index, variable = 'qtrly_estabs_count', dimension= 'industry', show = False, savepath = None)

    #     if single:
    #         vector = Vector(key = self.index, recession = 2001, dimension= dimension, variable = 'month3_emplvl', show = False)
    #         self.empl_2001 = vector.plot_single(colorcode = True, check = False)
    #         vector = Vector(key = self.index, recession = 2008, dimension= dimension, variable = 'month3_emplvl', show = False)
    #         self.empl_2008 = vector.plot_single(colorcode = True, check = False)
    #         vector = Vector(key = self.index, recession = 2001, dimension= dimension, variable = 'avg_wkly_wage', show = False)
    #         self.wage_2001 = vector.plot_single(colorcode = True, check = False)
    #         vector = Vector(key = self.index, recession = 2008, dimension= dimension, variable = 'avg_wkly_wage', show = False)
    #         self.wage_2008 = vector.plot_single(colorcode = True, check = False)
    #         vector = Vector(key = self.index, recession = 2001, dimension= dimension, variable = 'qtrly_estabs_count', show = False)
    #         self.firm_2001 = vector.plot_single(colorcode = True, check = False)
    #         vector = Vector(key = self.index, recession = 2008, dimension= dimension, variable = 'qtrly_estabs_count', show = False)
    #         self.firm_2008 = vector.plot_single(colorcode = True, check = False)

