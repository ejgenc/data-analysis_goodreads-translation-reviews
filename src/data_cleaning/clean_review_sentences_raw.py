# -*- coding: utf-8 -*-
"""
Created on Wed Dec 2 23:24:42 2020
@author: ejgen

------ What is this file? ------

This script ingests the file review_sentences_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/review_sentences_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/review_sentences_cleaned.csv
    
Reports related to the cleaning process are located at:
    ../../data/cleaning_reports/...

"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import csv
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/raw/review_sentences_raw.csv")
goodreads_reviews = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Cleaning: filter, document and drop null values ---



