# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:54:18 2021

@author: ejgen

This test module contains some data quality tests for the
goodreads_reviews_analyzed.csv file. the file can be found at:
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
    
"""

#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

# Test that VADER scores -1 >= x <= 1

# Test that percentage sums are within are 0 >= x <= 100