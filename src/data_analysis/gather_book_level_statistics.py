# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:49:35 2021

@author: ejgen

------ What is this file? ------

This script targets the files goodreads_reviews_analyzed.csv and related files,
gathering book level statistics about things like number of reviews on the
Goodreads website/number of reviews scraped, total/mean review length etch.

This script targets the following files:
    ../../data/external/book_data_external.xlsx
    ../../data/raw/goodreads_reviews_raw.csv
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
    
The resulting csv file is located at:
    ../../data/analysis_results/book_level_stats.csv

"""
#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

