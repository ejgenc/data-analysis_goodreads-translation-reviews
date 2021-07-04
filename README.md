# Seeking Traces of the Translator’s Invisibility in Goodreads Reviews

![Top twenty modifiers for the book - translation token pair.](https://github.com/ejgenc/data-analysis_goodreads_translation_reviews/blob/master/media/figures/processed/visualize_top_twenty_modifiers/book%20-%20translation.png)
_A sneak peek into the results of the analysis._

## What is this project about?

This repository contains the analysis code for my bachelor's graduation project *Seeking Traces of the Translator's Invisibility in Goodreads Reviews.* The Translator's Invisibility is a translation studies theory first introduced by the scholar Lawrence Venuti. It specifies and explains the dominant norm of "the invisible translator" that exists in the anglophone literary world. My bachelor's project seeks to find the traces of the translator's invisibility in the English translation reviews left on the social book review website Goodreads. It is a humanities data analysis project based on the the collection, processing, cleaning, analysis and the visualization of a corpus.

## Technical Details

The whole data analysis pipeline is written in Python. The project makes use of the following packages:

* [**Selenium**](https://selenium-python.readthedocs.io/), [**BeautifulSoup**](https://beautiful-soup-4.readthedocs.io/en/latest/): Web scraping and data ingestion.
* [**Pandas**](https://pandas.pydata.org/): For general data manipulation and data analysis.
* [**NLTK**](https://www.nltk.org/), [**SpaCy**](https://spacy.io/): For natural language processing tasks like dependency parsing.
* [**Matplotlib**](https://matplotlib.org/): For all the data visualizations. Used in conjunction with manual vector graphics editing.
* [**Doit**](https://pydoit.org/): Automation tool. Like [**Make**](https://www.gnu.org/software/make/), but Python native. Used to put all scripts in order.

Additionally, the [**Conda package manager**](https://docs.conda.io/en/latest/) was used for Python dependency and environment management. A Conda installation is required for those who wish to reproduce the analysis.

The code responsible for the analysis was split into separate categories such as **data processing, data cleaning, data analysis and data visualization**. Helper functions and utility scripts were also separated and organized accordingly. A separate script was created for each discernible step and then these scripts were organized using the **Doit** library. The Doit library offers crucial features such as task dependency checking, file dependency checking and analysis state calculation. These features help both during the development and the replication steps. The web scraping script serves as an entry point to the whole of the analysis. It feeds from an Excel file (.xlsx) in which the HTTP address of the books to scrape are specified. The main goal of the publication of this project's source code is enabling the reproduction of the original results as presented in the paper. However, those who wish to extend the analysis by targeting other Goodreads reviews can also attempt to do so. The Excel file is kept within the analysis for this purpose. **Please note that extending the analysis requires extra work, and extensions efforts as described below might end in failure if there is a change to the Goodreads data access**. Details on extending the analysis can be found in the **"How to extend this analysis?"** section below.

Data quality tests were written to check for quality errors (data type mismatch, null values, data out of expected range etc.). The tests were triggered after some data processing script executions and each data cleaning script executions.

The raw data and its subsequent versions are all saved as .csv files. Each variation of the original corpus is recorded for backtesting and reproduction purposes. Rows of data that are dropped during the cleaning process are also recorded separately. The replicator must follow the steps outlined below and replicate the analysis for the datasets to show up under their respective folders.

## How to reproduce this analysis?

The successful replication of this project requires the [**Conda package manager**](https://docs.conda.io/en/latest/). Before proceeding with the guide specified below, please make sure to have a recent version installed on your system.

#### 1.) Clone or download the project files

Before recreating the analysis environment and running the analysis, you need to have the project files on your computer. **You can download the source code of this project and the related material either through cloning the repository using a Git client, using GitHub desktop or through manual download.**

#### 2.) Recreate the environment that the analysis was conducted in

CD to the root of the project directory. Then run the following command in the Anaconda prompt (or any terminal where you can run the Conda package manager from from):

`conda env create -f environment.yml`

Running this command will make Conda create a new environment similar to the environment of the analysis with the information provided inside the **environment.yml** file. *goodreads-reviews-analysis_env* will be name of this new environment. **The specific Python version that the analysis was conducted in is also encoded into the environment.yml file.**

Once you are done, **don't forget to activate your environment before running the analysis.** You can activate the environment using the following command:

`conda activate goodreads-reviews-analysis_env`

#### 3.) Utilize the Python doit package to run the analysis

Doit is a handy tool in Python that can be used to automate certain tasks, including data analysis workflows. This project makes use of the Doit package to make replication easier. All the information related to the pipeline structure of the analysis is located in the **dodo.py** file.

To run the whole processing, cleaning, analysis and visualization process from start to finish, do the following:

* Open a Python interpreter or any command line tool you can run Python from.

* Activate the environment you have created in the previous step.

* cd to the root project folder, the folder in which the **dodo.py** file is located..

* Run the following commands in the following order: `doit forget` and then `doit`.

Whenever you want to re-run the analysis, repeat the two commands in the same order.

**Attention!** Running the whole pipeline on your computer skips two parts of the original analysis:

* Manual editing of the final data visualizations. **The data visualizations used in the paper were manually edited.** However, these changes are not major and you can verify the differences because the "raw" data visualizations will still be re-created.

* Scraping the web for raw translation reviews dataset. **This part is skipped on purpose to prevent the analysis from being corrupted due to a subsequent change in the website scraped.** Still, the cleaned version of the scraped dataset is provided with the source code. Those who wish to extend the analysis by re-scraping the specified books or scraping new books can do so following the guide below.

## How to extend this analysis?

As previously explained, the files provided by default are geared towards reproducing the results as presented in the project. Despite this, extending and/or changing the focus of analysis to other Goodreads reviews is possible. **Please note that there is NO guarantee that the extension methods presented below will work any time in the future.** Potential reasons of failure include a change in the Goodreads website, a change in the data format presented by Goodreads and the introduction of certain data points that fail the analysis pipeline. Extending the analysis requires:

* Editing the web scraping targets
* Unlocking hidden functionality
* Providing new login information for Goodreads
* Running the analysis pipeline

#### 1.) Edit the web scraping targets

Navigate to **data/external/...** and find the Excel file titled **book_data_external.xlsx.** This file is targeted by the web scraping script and it is used to specify the relevant Goodreads books. To change the books investigated by this analysis, **remove the whole desired row** or **add a new row with all the required information.** All column headers (http_id, http, book_id, book_name, author) must be filled in the order that they appear. 

#### 2.) Edit the dodo.py file

The **dodo.py** file is the scripts to be triggered are specified. By default the scripts responsible for the quality testing of the **book_data_external.xlsx** file, the web scraping, the cleaning and the quality testing of the raw data are commented out. In order to unlock this functionality, open the **dodo.py** file, find the commented out sections, uncomment them and then save the file. Carefully look at all of the file for sections tagged with **ATTENTION.**

#### 3.) Provide your own Goodreads login credentials

The scraping script logins to the Goodreads website in order to access the comments uninterrupted. You need to provide your own Goodreads login credentials in order to achieve this. Create a text file called **env.txt** in the root folder of project. Write the email you use to access Goodreads on the first line. Write your Goodreads password on the second. Save and exit the file.

#### 4.) Utilize the Python doit package to run the analysis

See the third item on the **"How to reproduce this analysis?** section for further information.

## Project  Organization

Below is a document tree of this project for those who wish to explore further.

--------
```
    |
    ├── data
    |   ├── analysis_results        <- Data analysis results, created through scripts in src/data_analysis/...    
    │   ├── cleaned                 <- Transformations of "raw" data created through scripts in src/data_cleaning/...
    │   ├── cleaning_reports        <- Datasets containing the data that has been dropped through the cleaning process.
    │   ├── external                <- Data not produced through any of the scripts in the codebase.
    │   └── raw                     <- Data produced through scripts in src/data_processing. Includes raw, inmutable data from web scraping.
    │
    |── media                       <- Contains internally generated figures. Internally generated figures come with a license.
    │    ├── figures                <- Data visualizations (both raw and processed) created for the presentation of this analysis.
    │           ├── processed       <- Edited versions of the raw data visualizations and custom-created visualizations.
    │           ├── raw             <- Unedited data visualizations created through the scripts in src/data_visualization/...
    |
    ├── reports                     <- Generated analysis as HTML, PDF, LaTeX, etc.
    |
    ├── src                         <- Source code of this project.
    │   ├── data_analysis           <- Scripts that analyze the cleaned datasets.
    |   |── data_cleaning           <- Scripts that clean the "raw" datasets resulting from data processing.                 
    │   |── data_processing         <- Scripts that gather data or to transform datasets into other datasets.
    |   |── data_visualization      <- Scripts that create visualizations.
    |   |── helper_functions        <- Scripts that contain various helper functions.
    |   |── utility_scripts         <- Scripts that aid in tasks such as analysis setup and teardown.
    |   
    ├── tests                       <- Contains test modules that test the data analysis pipeline.
    |   ├── data_quality_tests      <- Contains data quality tests that test cleaned datasets, analysis results etc.
    |          
    |── environment.yml             <- A .yml file for reproducing the analysis environment.
    |
    |── dodo.py                     <- A file that contains all the information needed to run automation package Doit.
    |
    |── setup.py                    <- A file that contains information about the packaging of the code.
    |
    |── .gitignore                  <- A file to specify which folders/files will be flagged with gitignore
    |
    ├── LICENSE                     < - Software license.
    |
    ├── README.md                   <- The top-level README for the users of this project.
    |
```
--------
