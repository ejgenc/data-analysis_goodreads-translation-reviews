# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:35:39 2021

@author: ejgen

------ What is this file? ------

This script targets the files goodreads_reviews_cleaned.csv and
review_sentences_analyzed.csv, calculating summary statistics such as
review length and sentiment score.

This script targets the following files:
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    ../../data/analysis_results/review_sentences_analyzed.csv
    
The resulting csv file is located at:
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
        
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

#goodreads_reviews_cleaned
import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
goodreads_reviews = pd.read_csv(import_fp, encoding = "utf-8")

#review_sentences_analyzed
import_fp = Path("../../data/analysis_results/review_sentences_analyzed.csv")
review_sentences_analyzed = pd.read_csv(import_fp, encoding = "utf-8", sep = ",")

