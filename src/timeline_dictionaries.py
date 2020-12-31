from produce_datasets import *


var_abbr = {'month3_emplvl': 'empl', 'avg_wkly_wage':'wage', 'qtrly_estabs_count':'firm'}

dim_abbr = {'industry':'indus', 'area':'area'}

#stores the relevant years for recessions. Will be expanded later.
recessions_str = {2001: ['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007'],
2008: ['2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']}

recessions_int = {2001: [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007],
2008: [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019],
'full': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]}

recession_events = {2001: 2001.75, 2008: 2008.75, 2020: 2020.25, 'full': None}

events_display = {2001: 'Sept 11', 2008: 'Financial Crash', 2020: 'COVID-19', 'full': None}

end_columns =  {2001:33, 2008:53, 'full':82}

#cleanup of quarter designations for better charts- 2001
quarters_display = {2000.25: 'Q1 2000', 2000.5: 'Q2 2000', 2000.75: 'Q3 2000', 2001.0: 'Q4 2000', 
2001.25: 'Q1 2001', 2001.5: 'Q2 2001', 2001.75: 'Q3 2001', 2002.0: 'Q4 2001', 
2002.25: 'Q1 2002', 2002.5: 'Q2 2002', 2002.75: 'Q3 2002', 2003.0: 'Q4 2002', 
2003.25: 'Q1 2003', 2003.5: 'Q2 2003', 2003.75: 'Q3 2003', 2004.0: 'Q4 2003', 
2004.25: 'Q1 2004', 2004.5: 'Q2 2004', 2004.75: 'Q3 2004', 2005.0: 'Q4 2004', 
2005.25: 'Q1 2005', 2005.5: 'Q2 2005', 2005.75: 'Q3 2005', 2006.0: 'Q4 2005', 
2006.25: 'Q1 2006', 2006.5: 'Q2 2006', 2006.75: 'Q3 2006', 2007.0: 'Q4 2006', 
2007.25: 'Q1 2007', 2007.5: 'Q2 2007', 2007.75: 'Q3 2007', 2008.0: 'Q4 2007', 
2008.25: 'Q1 2008', 2008.5: 'Q2 2008', 2008.75: 'Q3 2008', 2009.0: 'Q4 2008', 
2009.25: 'Q1 2009', 2009.5: 'Q2 2009', 2009.75: 'Q3 2009', 2010.0: 'Q4 2009', 
2010.25: 'Q1 2010', 2010.5: 'Q2 2010', 2010.75: 'Q3 2010', 2011.0: 'Q4 2010', 
2011.25: 'Q1 2011', 2011.5: 'Q2 2011', 2011.75: 'Q3 2011', 2012.0: 'Q4 2011', 
2012.25: 'Q1 2012', 2012.5: 'Q2 2012', 2012.75: 'Q3 2012', 2013.0: 'Q4 2012', 
2013.25: 'Q1 2013', 2013.5: 'Q2 2013', 2013.75: 'Q3 2013', 2014.0: 'Q4 2013', 
2014.25: 'Q1 2014', 2014.5: 'Q2 2014', 2014.75: 'Q3 2014', 2015.0: 'Q4 2014', 
2015.25: 'Q1 2015', 2015.5: 'Q2 2015', 2015.75: 'Q3 2015', 2016.0: 'Q4 2015', 
2016.25: 'Q1 2016', 2016.5: 'Q2 2016', 2016.75: 'Q3 2016', 2017.0: 'Q4 2016', 
2017.25: 'Q1 2017', 2017.5: 'Q2 2017', 2017.75: 'Q3 2017', 2018.0: 'Q4 2017', 
2018.25: 'Q1 2018', 2018.5: 'Q2 2018', 2018.75: 'Q3 2018', 2019.0: 'Q4 2018', 
2019.25: 'Q1 2019', 2019.5: 'Q2 2019', 2019.75: 'Q3 2019', 2020.0: 'Q4 2019', 
2020.25: 'Q1 2020', 2020.5: 'Q2 2020', 2020.75: 'Q3 2020', 2021.0: 'Q4 2020'}

class Recession(object):

    def __init__(self, year = 2008):
        self.years = recessions_int[year]
        self.event_year = year
        self.event_quarter = recession_events[year]
        self.event_label = events_display[year]
        self.quarters = [quarter for quarter in quarters_display.keys() if quarter >= min(self.years) and quarter <= (max(self.years) + 1)]
        self.xaxis = [v for k,v in quarters_display.items() if k in self.quarters]

    def compute_timelines(self, variables = ['month3_emplvl', 'avg_wkly_wage', 'qtrly_estabs_count'], dimensions = ['area', 'industry']):
        if 'area' in dimensions:
            if 'month3_emplvl' in variables:
                self.area_empl = create_timeline(variable = 'month3_emplvl', dimension = 'area', recession = self.event_year, save = False)
            if 'avg_wkly_wage' in variables:
                self.area_wage = create_timeline(variable = 'avg_wkly_wage', dimension = 'area', recession = self.event_year, save = False)
            if 'qtrly_estabs_count' in variables:
                self.area_firm = create_timeline(variable = 'qtrly_estabs_count', dimension = 'area', recession = self.event_year, save = False)
        if 'industry' in dimensions:
            if 'month3_emplvl' in variables:
                self.indus_empl = create_timeline(variable = 'month3_emplvl', dimension = 'area', recession = self.event_year, save = False)
            if 'avg_wkly_wage' in variables:
                self.indus_wage = create_timeline(variable = 'avg_wkly_wage', dimension = 'area', recession = self.event_year, save = False)
            if 'qtrly_estabs_count' in variables:
                self.indus_firm = create_timeline(variable = 'qtrly_estabs_count', dimension = 'area', recession = self.event_year, save = False)
 



    

