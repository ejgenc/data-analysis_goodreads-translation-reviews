# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 14:33:47 2021

@author: ejgen

------ What is this file? ------

This script targets the analysis result data that describes which 
unique modifiers have been used for which modified groups (author/translator etc.)
how many times. The script produces a horizontal bar chart for each
modified group. The number of occurence of each unique modifier is encoded
by using position on a common scale(y-axis) / bar length. The same information
is reduntantly encoded with textual annotation. Categorical information about
modifier classification (positive - neutral - negative) is encoded using color
hue. The said hue is applied on both the variables names, the data markers
and textual annotation. Summary statistics is presented in text.

This script targets the following files:
    ../../data/analysis_results/total_modifiers_per_modified_group.csv
    ../../data/analysis_results/total_modifiers_per_unique_modified.csv
    ...
    
    
The resulting raw figures are located at:
    ../../media/figures/raw/visualize_modifiers/*
"""

#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import pandas as pd
import matplotlib.pyplot as plt

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/analysis_results/"
                 "group_refers_to_author_modifier_value_counts.csv")

test = pd.read_csv(import_fp)

