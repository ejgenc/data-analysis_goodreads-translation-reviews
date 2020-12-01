# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This script ingests the file goodreads_reviews_cleaned.csv in order to process
it into a second level or analysis

This script targets the following file:
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    
The resulting csv file is located at:
    ../../data/raw/review_sentences_raw.csv
    
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

import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
goodreads_reviews = pd.read_csv(import_fp)

