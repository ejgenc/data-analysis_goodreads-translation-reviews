# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:48:42 2020

@author: ejgen

------ What is this file? ------

This script ingests the file tokens_and_dependencies_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/tokens_and_dependenciees_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/tokens_and_dependencies_cleaned.csv
    
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

import_fp = Path("../../data/raw/tokens_and_dependencies_raw.csv")
tokens_and_dependencies = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Cleaning: filter, document and drop null values ---

#Create masks for null values and non-null values
null_values_mask = tokens_and_dependencies.isnull()

# null_values_mask.sum().sum() != 0, so there are null values

#Use the mask to single out the null values
# Select rows where there is at least one True

tokens_and_dependencies_rows_with_null_values = tokens_and_dependencies[null_values_mask.any(axis = 1)].reset_index(drop = True)

#Use the reverse of the mask to select rows in which all columns are TRUE
tokens_and_dependencies = tokens_and_dependencies[~(null_values_mask.any(axis = 1))].reset_index(drop = True)

#%% --- Cleaning: assure data type agreement between and within columns ---

error_list = []

for column_name in tokens_and_dependencies.columns:
    expected_dtype = type(tokens_and_dependencies[column_name][0])
    value_index = 0
    while value_index < len(tokens_and_dependencies[column_name]):
        actual_dtype = type(tokens_and_dependencies[column_name][value_index])
        if expected_dtype != actual_dtype:
            error_entry = [column_name, value_index, expected_dtype, actual_dtype]
            error_list.append(error_entry)
        value_index += 1
        
# There appears to be no proof of data-type disagreement. Moving on.

#%% --- Export Data ---

export_fp = Path("../../data/cleaned/tokens_and_dependencies_cleaned.csv")
tokens_and_dependencies.to_csv(export_fp, encoding = "utf-8", index = False)
            
#%% --- Export cleaning documentation - that has been deleted ---

export_fp = Path("../../data/cleaning_reports/tokens_and_dependencies_rows_with_null_values.csv")
tokens_and_dependencies_rows_with_null_values.to_csv(export_fp, encoding = "utf-8", index = False)