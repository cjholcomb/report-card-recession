
from flask import Flask, render_template, url_for, flash, redirect, request, session, make_response
from charting import *

import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

@app.route('/')
def landing():
    return render_template('lookup_indus.html')

@app.route('/lookup_indus', methods = ['GET'])
def industry_search():
    return render_template('lookup_indus.html')

@app.route('/results', methods = ['GET','POST'])
def results():
    code = int(request.form['industry_code'])
    
    #compute key metrics
    industry = Industry(code)
    title = industry.title
    stats = produce_stats(code)

    #produce charts
    objective_charts(code)
    subjective_charts(code)

    return render_template('results.html', code = code, title = title, stats = stats)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)


# @app.route('/static/images/varcomp_2001.png')
# def varcomp_2001():
#     fig = variable_comparison(key = code, recession= 2001, dimension= 'industry')
#     plt.savefig('/static/images/varcomp_2001.png')
#     return fig

# @app.route('/results', methods = ['GET','POST'])
# def results():
#     code = request.form['industry_code']
#     # industry = Industry(code)
#     return render_template('results.html', code = code)

    # fips = str(request.form['fips'])
    # area = Area(fips, df_2001, df_2008, df_2020)
    # return render_template('results.html',
    #  fips = fips,
    #  title = area.title,
     
    #  nadir_2001 = area.nadir_2001,
    #  pre_peak_2001 = area.pre_peak_2001,
    #  post_peak_2001 = area.post_peak_2001,
     
    #  recov_2001 = area.recovery_2001,
    #  growth_2001 = area.growth_2001,
    #  decline_2001 = area.decline_2001,

    #  y_2001 = area.y_2001,
    # #  timeline_2001 = area.plot_2001(),
     
    #  nadir_2008 = area.nadir_2008,
    #  pre_peak_2008 = area.pre_peak_2008,
    #  post_peak_2008 = area.pre_peak_2008,

    #  recov_2008 = area.recovery_2008,
    #  growth_2008 = area.growth_2008,
    #  decline_2008 = area.decline_2008,
     
    #  y_2008 = area.y_2008,
    # #  timeline_2008 = area.plot_2008(),

    #  forecast = area.forecast,
    #  jobs = area.jobs_2020,




# @app.route('/static/images/plot_2001.png')
# def plot_2001():
#     fig, ax = plt.subplots(figsize = (12,4))
#     x = quarters_2001.values()
#     y = area.y_2001
#     ax.plot(x,y, color = 'green', linewidth = 1, alpha = 0.8)
#     ax.axhline(y = area.nadir, xmin = 'Q1 2000', xmax = 'Q4 2007', 
#                 color = 'red', linewidth = .5, alpha = 0.5, label = 'nadir')
#     ax.axhline(y = area.pre_peak, xmin = 'Q1 2000', xmax = 'Q4 2007',
#                 color = 'blue', linewidth = .5, alpha = .5)
#     ax.tick_params(axis='both', which='major', labelsize=10)
#     ax.tick_params(axis='both', which='minor', labelsize=10)
#     ax.legend(fancybox = True, borderaxespad=0)
#     plt.savefig('/static/images/plot_2001.png')
#     return fig, ax



# @app.route('/dataset')
# @app.route('/data-dictionary')
# @app.route('/exploratory-data-analysis')
# @app.route('/model-tuning')
# @app.route('/feature-importance')
# @app.route('/predicted-outcomes')

# @app.route('/industry-lookup')


    
#     quarters_2001 = {'2000.25': 'Q1 2000', '2000.5': 'Q2 2000', '2000.75': 'Q3 2000', '2001.0': 'Q4 2000', 
#                 '2001.25': 'Q1 2001', '2001.5': 'Q2 2001', '2001.75': 'Q3 2001', '2002.0': 'Q4 2001', 
#                 '2002.25':'Q1 2002', '2002.5':'Q2 2002', '2002.75':'Q3 2002', '2003.0':'Q4 2002',
#                 '2003.25':'Q1 2003', '2003.5':'Q2 2003', '2003.75':'Q3 2003', '2004.0':'Q4 2003', 
#                 '2004.25':'Q1 2004', '2004.5':'Q2 2004', '2004.75':'Q3 2004', '2005.0':'Q4 2004', 
#                 '2005.25':'Q1 2005', '2005.5':'Q2 2005', '2005.75':'Q3 2005', '2006.0':'Q4 2005',
#                 '2006.25':'Q1 2006', '2006.5':'Q2 2006', '2006.75':'Q3 2006', '2007.0':'Q4 2006',
#                 '2007.25':'Q1 2007', '2007.5':'Q2 2007', '2007.75':'Q3 2007', '2008.0':'Q4 2007'}

#     quarters_2008 = {
#                 '2007.25':'Q1 2007', '2007.5':'Q2 2007', '2007.75':'Q3 2007', '2008.0':'Q4 2007', 
#                 '2008.25':'Q1 2008', '2008.5':'Q2 2008', '2008.75':'Q3 2008', '2009.0':'Q4 2008',
#                 '2009.25':'Q1 2009', '2009.5':'Q2 2009', '2009.75':'Q3 2009', '2010.0':'Q4 2009',
#                 '2010.25':'Q1 2010', '2010.5':'Q2 2010', '2010.75':'Q3 2010', '2008.0':'Q4 2010',
#                 '2011.25':'Q1 2011', '2011.5':'Q2 2011', '2011.75':'Q3 2011', '2012.0':'Q4 2011',
#                 '2012.25':'Q1 2012', '2012.5':'Q2 2012', '2012.75':'Q3 2012', '2013.0':'Q4 2012',
#                 '2013.25':'Q1 2013', '2013.5':'Q2 2013', '2013.75':'Q3 2013', '2014.0':'Q4 2013',
#                 '2014.25':'Q1 2014', '2014.5':'Q2 2014', '2014.75':'Q3 2014', '2015.0':'Q4 2014',
#                 '2015.25':'Q1 2015', '2015.5':'Q2 2015', '2015.75':'Q3 2015', '2016.0':'Q4 2015',
#                 '2016.25':'Q1 2016', '2016.5':'Q2 2016', '2016.75':'Q3 2016', '2017.0':'Q4 2016',
#                 '2017.25':'Q1 2017', '2017.5':'Q2 2017', '2017.75':'Q3 2017', '2018.0':'Q4 2017',
#                 '2018.25':'Q1 2018', '2018.5':'Q2 2018', '2018.75':'Q3 2018', '2019.0':'Q4 2018',
#                 '2019.25':'Q1 2019', '2019.5':'Q2 2019', '2019.75':'Q3 2019', '2020.0':'Q4 2019'}
#     df_full = pd.read_json('data/training_dataset.json')
#     df_2001 = pd.read_json('data/Recession1_timeline.json')
#     df_2001 = df_2001.set_index('area_fips')
#     df_2001 = df_2001.rename(columns = quarters_2001)
#     df_2008 = pd.read_json('data/Recession2_timeline.json')
#     df_2008 = df_2008.set_index('area_fips')
#     df_2008 = df_2008.rename(columns = quarters_2008)
#     df_2020 = pd.read_json('data/prediction_2020.json')

# @app.route('/', methods = ['GET', 'POST'])
# @app.route('/index')
# @app.route('/home')
# @app.route('/table-of-contents')
# @app.route('/contents')
# def contents():
#     return render_template('index.html', areas = test)

# @app.route('/overview')
# def overview():
#     return render_template('overview.html')

# @app.route('/dataset')
# @app.route('/data')
# def data():
#     return render_template('data.html')

# @app.route('/exploratory-data-analysis')
# @app.route('/EDA')
# def eda():
#     return render_template('EDA.html')


# @app.route('/models')
# def models():
#     return render_template('models.html')

# @app.route('/lookup_area', methods = ['GET'])
# def fips_search():
#     return render_template('lookup_area.html')






     

# @app.route('/2001')
# def map_2001: