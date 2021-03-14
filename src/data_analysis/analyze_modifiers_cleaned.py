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

#%% --- Analyze: find how many modifiers have been used per modified group ---

# !!! NOTE !!!
# Remember to .reset_index() after these groupby + agg 
# operations to keep a more sensible dataframe

# !!! NOTE !!!
# Look at the syntax below carefully. It is a good way to chain methods
# in pandas. First, I am declaring that a variable is a dataframe.
# This way, I don't need to use inplace = True on the subsequent
# argument. In fact, doing so breaks the method chaining.
# I wrapped the expression around () to be able to chain without saying x\
# I can also use .pipe somewhere to chain my own methods / non/df native methods

# !!! NOTE !!!
# Previously, the modifier_counts dataframe was two seperate dataframes
# However, I remembered that you can actually used .agg() function
# to save it all into one dataframe. Lol

modifier_counts = (modifiers_grouped
                   .agg(["count","nunique"])
                   .reset_index()
                   .rename({"count":"number_of_nonunique_modifiers",
                            "nunique":"number_of_unique_modifiers"},
                           axis = 1)
                   .sort_values(by = "number_of_nonunique_modifiers",
                                ascending = False))

modifier_counts["unique_to_nonunique_ratio"] = (modifier_counts["number_of_unique_modifiers"] /
                                                modifier_counts["number_of_nonunique_modifiers"])

#%% --- Analyze: find how many times each modifier has been used per modified group ---                                 ---

modifier_value_counts_per_modified = {}

for group in modifiers_grouped.groups:
    group_value_counts = (modifiers_grouped.get_group(group)
                          .value_counts()
                          .reset_index()
                          .rename({"index":"modifier",
                                   "modifier":"count"},
                                  axis = 1)
                          .sort_values(by = "count",
                                       ascending = False))
    modifier_value_counts_per_modified[group] = group_value_counts
    
#%%

# This might work with merge?

trans_group = {"refers_to_translation":["translation","translations"]}
concatenated_value_counts = {}
for key,value in trans_group.items():
    to_concat = []
    for modified_name,series in modifier_value_counts_per_modified.items():
        if modified_name in value:
            to_concat.append(series)
    concatenated_value_counts[key] = pd.concat(to_concat)
            
    