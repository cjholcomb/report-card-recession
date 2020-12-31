<h1>Project Overview</h1>
                <p>The U.S. in the 21st century is not particularly adept at recovering from recessions, and another one is upon us. This recession is likely to be deeper and longer than the last. Traditional measures of economic health (unemployment, GDP, stock market) are all too aggregated to be of much use for most Americans. Overall rise and/or fall does nothing for the outlook of a particular town or city, nor does it speak to the resilency of particular economic sectors in the face of a recession. </p>
                <p>This project is a continuation of my capstone work for the Galvanize Data Sceince Immersive. While the previous iteration was a success given its time constraints, I want to expand the project to provide a scalable framework for working with QCEW data, and use it to analyze the trends in recessions in the US.</p>
                <p>While modeling the recovery from the 2020 COVID-19 recession was the initial goal, I have expanded the scope to include making a scalable, reusable library for working with QCEW data.</p>
    <h2>Project Goals</h2>
                    <ol type = "1">
                        <li>Develop an object-oriented module to define parameters of recessions, industries, and areas.</li>
                        <li>Expand parameters of the dataframe construction module to allow for automated construction of a timeline on any recession across any dimension(industry, area) or target variable (employment, wages, or firms).</li>
                        <li>Develop a module to automate charting of timelines.</li>
                        <li>Automate adjustment of NCAIS industry classifcation changes into the timeline data and ensure consistency across recession timelines.</li>
                        <li>Develop a version of the "scariest chart", atuomated to include any dimension, variable, or recession.</li>
                        <li>Update the Flask interface to include new charts and features.</li>
                        <li>Create an AWS instance to allow others to run report cards on areas or industries.</li>
                        <li>Expand data collection to include political, fiscal, and population data for areas.</li>
                        <li>Experiment with neural networks to model economic recovery with the new dimensions</li>
                        <li>Add previous recessions as possible parameters.</li>
                        <li>Update report card to include model projections</li>
                    </ol>
<h1>Data Source</h1>
                <p>The dataset is compiled from the  Bureau of Labor Statistics(BLS) Quarterly Census of Employment and Wages (QCEW). The BLS archives contain economic data stretching back decades, across geographic designations and NCAIS industry classifcations.<p>
                <p> Data can be downloaded <a href = "https://www.bls.gov/cew/downloadable-data-files.htm">here</a>.</p>
                <p>While employment numbers are available on a monthly basis, wages and establishments only have quarterly data. Therefore, I will primarily be working with quarterly timelines.
    <h2>Instructions for downloading data</h2>
                <p>The code makes several assumptions about the folder structure and file names. Follow these instructions to make sure the data is in a readblae state by the code.</p>
                    <ul>
                        <li>Create "industry_files" and "area_files" folders in the data/ folder.</li>
                        <li>Download a file archive from the "CSVs By Area-->Quarterly" or the "CSVs By Industry-->Quarterly". The archive will contain many files, but you only need the total file included in each.</li> 
                        <li>Save that file in the relevant folder. <b> Note: Files that belong in the Industry folder will be found in the Area column, and vice-versa.</b> This is because the Total file will be the total for across areas/industries, with breakdowns by the other dimension.</li>
                        <li>Rename the file to only the four-digit year, retaining the .csv extension.</li>
                    </ul>
<h1>Definitions</h1>
                <p>The below chart is the inspiration for this project, and may help contextualize some of the defintitions below.</p>
                    <img src="src/static/images/ScariestJan2017.PNG" alt="Job Losses"></img>
    <h2>Recession</h2>
                <p>Recession parameters are stored in recessions.py 
                <p>Recessions are defined by economists, and while there is some debate on the qualifications of a recession, for simplicity's sake I will use the defined recessions included in the graph.</p>
                <p>In order to capture the information required, the timelines in question include the <i> full calendar year before the recession event </i>, extending to the <i>full calendar year prior to the <b>next</b> recession event</i>. While the recession officially ends long before that, not every area/industry recovers on that timeline, and we must capture that information.
        <h3>Recession Event</h3>
                <p>An event popularly conbsidered to be a catalyst for the recession.   
        <h3>Included Recessions</h3>
                    <ul>
                        <li><b>2001</b>- Timeline: 2000-2007. Event: Sept 11, Q3 2001. </li>
                        <li><b>2008</b>- Timeline: 2007-2019. Event: Financial Crisis, Q3 2008. </li>
                        <li><b>Full</b>: Timeline: 2007-2019. This designation exists only to produce timelines across all recessions included.</li>
                    </ul>
    <h2>Dimension</h3>
        <h3>Area</h3>
                <p>Area parameters are stored in area.py
                <p>The BLS data includes four different types of area designations:
                    <ul>
                        <li>National: The full United States economic data. There are also designations for Metropolitan and Non-Metropolitan areas.
                        <li>State: One of fifty recognized states. This also includes Puerto Rico and the U.S. Virgin Islands
                        <li>County: County designations within states. This includes Puerto Rican municipios and individual islands within the U.S. Virgin Islands
                        <li>Metropolitan Statistical Area: Cities within the US.
                        <li>Combined Stastical Area: Wider definitions to capture populous areas across cities and even state lines.
                    </ul>
                <p><b>area_fips</b>(str) is the index for areas.
                <p>More information can be found <a href = "https://www.bls.gov/cew/classifications/areas/area-guide.htm">here.</a>
        <h3>Industry</h3>
                <p>Industry parameters are stored in industries.py
                <p>Industries are defined according to NAICS. The data is hierarchicical and quite complex. Broad-encompassing industries are broken down into more granular ones lower in the hierarchy.
            <h4>Child Industry</h4>
                <p>When an industry is broken down into more smaller industries, I am defining each of those as a child industry
            <h4>Parent Industry</h4>
                <p> The industry a child industry comes from.
            <h4>Sibling Industries</4>
                <p>The set of child industries from a single parent industry.
            <h4>Generation</h4>
                <p>Where in the industry hierarchy an industry falls.
                <p><b>industry_code</b>(int) is the index for industries.
                <p>More information can be found <a href = "https://www.bls.gov/cew/classifications/industry/home.htm">here.</a>
        <h3>Potential future dimensions to add to the project:</h3>
                    <ul>
                        <li>Population(U.S. Census)
                        <li>State budgets
                        <li>Partisan control of government
                    </ul>
    <h2>Targets</h2>
                <p>One of the three targets (referred to as variables in the code) that is used to judge economic health.
        <h3>Employment</h3>
                <p>The number of jobs in each industry/area. In this project, I will only be using quarterly numbers.
                <p><i>Column Name: month3_emplvl</i>
        <h3>Wages</h3>
                <p>The average weekly wage in each industry/area.
                <p><i>Column Name: avg_wkly_wage</i>
        <h3>Establishments/Firms</h3>
                <p>The number of firms operating in each industry/area.
                <p><i>Column Name: qtrly_estabs_count</i>
<h1>Goals Progress</h1>
    <h2>1. Object-Oriented Approach</h2>
                <p>area.py, recessions.py, and industries.py each contains variable constants referred to throughout the project, and a class to define and store important parameters for analysis. These will continue to be expanded as the project evolves.
    <h2>2. Dataframe Construction Refactor </h2>
                <p>produce_datasets has been streamlined, depreciated code moved to the dpereciated code file. helper_functions.py has been depreciated, functions moved to produce_datasets.py.
                <p>The main function (create_timeline) has new parameters and options. It can now function on any target, dimension, or recession. It also contains options one whether or not to save the dataframe as a json file, as well as derive the variables listed below. (Derived variables greatly increase computing time).
        <h3>Derived Variables:</h3>
                <p>The below variables are computed based on the recession timelines</p>
                    <ul>
                        <li>nadir: The low point in the timeline. Excludes the first seven columns when computing.</li>
                        <li>nadir_qtr: The number of quarters (from the beginning of the timeline) until the nadir.</li>
                        <li>pre-peak: The high point of the timeline <i>before</i> the nadir.</li>
                        <li>pre_peak_qtr: The number of quarters (from the beginning of the timeline) until the pre-peak.</li>
                        <li>post-peak: The high point of the timeline <i>after</i> the nadir.</li>
                        <li>post_peak_qtr: The number of quarters (from the nadir) until the post-peak.</li>
                        <li>recovery: Whether or not the timeline recovers from the recession before the end of the timeline (Is post-peak >= pre-peak). 
                        <li>recovery_qtr: the number of quarters between the andir and when the timeline surpasses the pre-peak. Will be NaN if recovery == 0.
                        <li>decline: the number of quarters between the pre-peak and the nadir.
                        <li>delta: the difference between pre-peak and post-peak.
                    </ul>
    <h2>
            

 
    