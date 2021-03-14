# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 12:40:55 2021

@author: ejgen

------ What is this file? ------

This script ingests the file modifiers_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/cleaned/modifiers_cleaned.csv
    
The resulting csv files are located at:
    CSV FILES HERE
    
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

import_fp = Path("../../data/cleaned/modifiers_cleaned.csv")
modifiers_cleaned = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Prepare: create a groupby of modifieds and select modifiers ---

#Create a groupby
groupby_modified = modifiers_cleaned.groupby("modified")
#select modifiers
modifiers_grouped = groupby_modified["modifier"]

#%% --- Analyze: find how many modifiers have been used per each ---
#   --- modified group.                                          ---

non_unique_modifiers_count = modifiers_grouped.count()

#%% --- Analyze: find how many unique modifiers have been used   ---
#   --- per each modified group.                                 ---

unique_modifiers_count = modifiers_grouped.nunique()

#%% --- Analyze: find how many times each modifier has been used ---
#   --- per modified group.                                      ---

modifier_value_counts_per_modified = {}

for group in modifiers_grouped.groups:
    group_value_counts = modifiers_grouped.get_group(group).value_counts()
    modifier_value_counts_per_modified[group] = group_value_counts
    