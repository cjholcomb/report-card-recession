import os
import urllib.request 
import zipfile

url = {2010:'https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv',
2000:'http://www2.census.gov/programs-surveys/popest/datasets/2000-2010/intercensal/county/co-est00int-tot.csv',
1990:'https://www2.census.gov/programs-surveys/popest/tables/1990-2000/estimates-and-change-1990-2000/2000c8_00.txt',
1980:'https://www2.census.gov/programs-surveys/popest/tables/1980-1990/counties/totals/e8089co.txt',
1970:'https://www2.census.gov/programs-surveys/popest/tables/1900-1980/counties/totals/e7079co.txt'
}

filetype = {2010:'.csv', 2000:'.csv', 1990:'.txt', 1980:'.txt', 1970:'.txt'}

def create_filepaths():
    if not os.path.exists('data/source_files'):
        os.mkdir('data/source_files')
    if not os.path.exists('data/source_files/QCEW'):
        os.mkdir('data/source_files/QCEW')
    if not os.path.exists('data/source_files/QCEW/area_QCEW'):
        os.mkdir('data/source_files/QCEW/area_QCEW')
    if not os.path.exists('data/source_files/QCEW/industry_QCEW'):
        os.mkdir('data/source_files/QCEW/industry_QCEW')
    if not os.path.exists('data/source_files/census'):
        os.mkdir('data/source_files/census')
    if not os.path.exists('data/source_files/census/county'):
        os.mkdir('data/source_files/census/county')
    if not os.path.exists('data/source_files/census/city'):
        os.mkdir('data/source_files/census/city')

def download_QCEW(dimensions, years, override = False):
    """
    Downloads and extracts archived QCEW data. Archive (.zip) files are downloaded one at a time and removed before the next file is downloaded. Can require up to ~10 gigs of disk space
    
    Parameters: 
        dimensions (list, must be 'area' and/or 'industry'): determines if area or industry files are to be saved.
        years (list): years of data to be downloaded.
        override (bool): determines if files will be overriden if they already exist in the appropriate folder.

    Returns: 
        Nothing
    """
    create_filepaths()
    for dimension in list(dimensions):  
        for year in years:
            year = str(year)
            #derive download urls and save paths
            if dimension == 'area':
                if int(year) < 1990:
                    url = 'https://data.bls.gov/cew/data/files/' + year +'/csv/' +year + '_qtrly_naics10_totals.zip'
                    extractfolder = ''
                    extractname = year + '.q1-q4 10 Total, all industries.csv'
                elif int(year) in [2016, 2017, 2018, 2019]:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_industry.zip'
                    extractfolder = year + '.q1-q4.by_industry/'
                    extractname = year + '.q1-q4 10 10 Total, all industries.csv'
                elif int(year) == 2020:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_industry.zip'
                    extractfolder = year + '.q1-q2.by_industry/'
                    extractname = year + '.q1-q2 10 10 Total, all industries.csv'
                else:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_industry.zip'
                    extractfolder = year + '.q1-q4.by_industry/'
                    extractname = year + '.q1-q4 10 Total, all industries.csv'
            elif dimension == 'industry':
                if int(year) < 1990:
                    url = 'https://data.bls.gov/cew/data/files/' + year +'/sic/csv/sic_' + year+ '_qtrly_by_area.zip'
                    extractfolder = 'sic.' + year + '.q1-q4.by_area/'
                    extractname = 'sic.' + year + '.q1-q4 US000 (U.S. TOTAL).csv'
                elif int(year) == 2020:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_area.zip'
                    extractfolder = year + '.q1-q2.by_area/'
                    extractname = year + '.q1-q2 US000 U.S. TOTAL.csv'
                else:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_area.zip'
                    extractfolder = year + '.q1-q4.by_area/'
                    extractname = year + '.q1-q4 US000 U.S. TOTAL.csv'   
            dimension_long = 'data/source_files/QCEW/' + dimension + '_QCEW/'
            zipname = dimension_long + year + '.zip'

            #checks if file already exists
            if not override:
                if os.path.isfile(dimension_long + year + '.csv'):
                    print(dimension_long + year + '.csv already exists')
                    continue      

            #creates new folder
            if not os.path.isdir(dimension_long):
                os.mkdir(dimension_long)
            
            #downloads full zip files
            if os.path.isfile(zipname):
                print(year + '.zip already downloaded')
            else:
                urllib.request.urlretrieve(url, zipname)
                print(zipname + ' downloaded from ' + url)
            
            #extracts the file
            archive = zipfile.ZipFile(zipname)
            # print(extractfolder+extractname)
            archive.extract(extractfolder + extractname, path = dimension_long)
            os.rename(dimension_long + extractfolder + extractname,  dimension_long + year + '.csv')
            print(dimension_long + year + '.csv unpacked')
            
            #cleans up
            if not os.listdir(dimension_long + extractfolder):
                os.rmdir(dimension_long + extractfolder)
            os.remove(dimension_long + year + '.zip')
            print('files cleaned up')

def download_census(decades = [1970, 1980, 1990, 2000, 2010], counties = True, cities = True):
    create_filepaths()
    if counties:
        for decade in decades:
            urllib.request.urlretrieve(url[decade], 'data/source_files/census/county/' + str(decade) + filetype[decade])
            print('data/source_files/census/county/' + str(decade) + filetype[decade] + ' saved.')
        
def download_all(NAICS = True, SIC = False, override = False):
    '''
    Downloads all existing .csv files on the QCEW website.

    Parameters: 
        NAICS (bool, default True): determines if NAICS industry classification time period will be included (1990-present)
        SIC (bool, default False): determines if SIC industry classification time period will be included (1975-1989). 1990-2000 not included as the NAICS data files encompass this period. 
    
    Returns:
        Nothing
    '''

    years = []
    decades = []
    if NAICS:
        years.extend(list(range(1990, 2021)))
        decades.extend(list(range(1990, 2020, 10)))
    if SIC:
        years.extend(list(range(1975, 1990)))
        decades.extend(list(range(1970, 1990, 10)))
    download_QCEW(years = years, dimensions = ['area', 'industry'], override = override)
    download_census(decades = decades, counties = True, cities = True)