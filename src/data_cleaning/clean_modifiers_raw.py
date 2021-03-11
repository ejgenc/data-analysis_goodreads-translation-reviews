# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 22:45:18 2021

@author: ejgen

------ What is this file? ------

This script ingests the file modifiers_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/modifiers_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/modifiers_cleaned.csv
    
Reports related to the cleaning process are located at:
    ../../data/cleaning_reports/...
    
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

import_fp = Path("../../data/raw/modifiers_raw.csv")
modifiers = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Cleaning: filter, document and drop null values ---

#Create a mask for null values
null_values_mask = modifiers.isnull()

# null_values_mask.sum().sum() != 0, so there are null values

#%% --- Cleaning: assure data type agreement between and within columns ---

error_list = []

for column_name in modifiers.columns:
    expected_dtype = type(modifiers[column_name][0])
    value_index = 0
    while value_index < len(modifiers[column_name]):
        actual_dtype = type(modifiers[column_name][value_index])
        if expected_dtype != actual_dtype:
            error_entry = [column_name, value_index, expected_dtype, actual_dtype]
            error_list.append(error_entry)
        value_index += 1
        
# There appears to be no proof of data-type disagreement. Moving on.

#%% --- Cleaning: drop specific modifiers that are known false positives ---

#%% --- Cleaning: clean modified variation ---

#DO THIS NEXT: create a detailed list of all permissible forms
# check existing form match with permissible forms. Drop all that isn't.

#modified_variations = modifiers["modified"].unique()

#%% --- Export data ---

#%% --- Export cleaning documentation ---


