# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:05:50 2021

@author: ejgen

This test module contains some data quality tests for the
goodreads_reviews_analyzed.csv file. the file can be found at:
    ../../data/analysis_results/book_level_statistics.csv
    
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
