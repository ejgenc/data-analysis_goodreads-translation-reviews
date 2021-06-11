# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:42:07 2021

@author: ejgen

------ What is this file? ------

This script visualizes how many authors are represented in the corpus with n
book (n being 1, 2, 3, 4, 9). The script produces a dot plot, where dots can
be placed side to side in rows of three. The emergent pattern resembles a
bar chart and that is indeed the intended effect. The resulting plot is
less accurate than a bar chart and the data is visually "distorted." However,
here precision and truthfulness is not as important because the data is rather
minimal.

NOTE: The result requires some editing.

This script targets the following file:
    ../../data/analysis_results/book_level_statistics.csv
    ../../data/analysis_results/total_modifiers_per_unique_modified.csv
    ...
    
    
The resulting raw figures are located at:
    ../../media/figures/raw/visualize_bookcount_per_author/*
"""
#%% --- Import required packages ---

import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

input_fp = Path("../../data/analysis_results/book_level_statistics.csv")
dataset = (pd
            .read_csv(input_fp, encoding = "utf-8")
            .loc[:,:])

