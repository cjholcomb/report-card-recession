import os
import urllib.request 
import zipfile

def download_files(dimensions, years, override = False):
    """
    Downloads and extracts archived QCEW data. Archive (.zip) files are downloaded one at a time and removed before the next file is downloaded. Can require up to ~10 gigs of disk space
    
    Parameters: 
        dimensions (list, must be 'area' and/or 'industry'): determines if area or industry files are to be saved.
        years (list): years of data to be downloaded.
        override (bool): determines if files will be overriden if they already exist in the appropriate folder.

    Returns: 
        Nothing
    """
    for dimension in dimensions:  
        for year in years:
            year = str(year)
            #derive download urls and save paths
            if dimension == 'area':
                if int(year) <1990:
                    url = 'https://data.bls.gov/cew/data/files/' + year +'/csv/' +year + '_qtrly_naics10_totals.zip'
                else:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_industry.zip'
                if year == '2020':
                    extractfolder = year + '.q1-q2.by_industry/'
                    extractname = year + '.q1-q2 10 Total, all industries.csv'
                else:
                    extractfolder = year + '.q1-q4.by_industry/'
                    extractname = year + '.q1-q4 10 Total, all industries.csv'
            elif dimension == 'industry':
                if int(year) < 1990:
                    url = 'https://data.bls.gov/cew/data/files/' + year +'/sic/csv/sic_' + year+ '_qtrly_by_industry.zip'
                else:
                    url = 'https://data.bls.gov/cew/data/files/' + str(year) + '/csv/' + str(year) + '_qtrly_by_area.zip'
                if year == 2020:
                    extractfolder = year + '.q1-q2.by_area/'
                    extractname = year + '.q1-q2 US000 U.S. TOTAL.csv'
                else:
                    extractfolder = year + '.q1-q4.by_area/'
                    extractname = year + '.q1-q4 US000 U.S. TOTAL.csv'   
            dimension_long = 'data/' + dimension + '_files/'
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
            archive.extract(extractfolder + extractname, path = dimension_long)
            os.rename(dimension_long + extractfolder + extractname,  dimension_long + year + '.csv')
            print(dimension_long + year + '.csv unpacked')
            
            #cleans up
            os.rmdir(dimension_long + extractfolder)
            os.remove(dimension_long + year + '.zip')
            print('files cleaned up')

def download_all(NAICS = True, SIC = False):
    '''
    Downloads all existing .csv files on the QCEW website.

    Parameters: 
        NAICS (bool, default True): determines if NAICS industry classification time period will be included (1990-present)
        SIC (bool, default False): determines if SIC industry classification time period will be included (1975-1989). 1990-2000 not included as the NAICS data files encompass this period. 
    
    Returns:
        Nothing
    '''

    years = []
    if NAICS:
        years.extend(list(range(1990, 2021)))
    if SIC:
        years.extend(list(range(1975, 1990)))
    download_files(years = years, dimensions = ['area', 'industry'])