# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:45:43 2020

------ What is this file? ------
                
This script ingests the file review_sentences_cleaned.csv in order to transform
it into another dataset.

This script targets the following file:
    ../../data/cleaned/review_sentences_cleaned.csv
    
The resulting csv file is located at:
    ../../data/raw/relevant_words_raw.csv
    
"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import nltk

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/review_sentences_cleaned.csv")
review_sentences = pd.read_csv(import_fp)

#%% --- 