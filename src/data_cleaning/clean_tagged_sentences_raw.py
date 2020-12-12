# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:08:50 2020

@author: ejgen

------ What is this file? ------

This script ingests the file tagged_sentences_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/tagged_sentences_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/tagged_sentences_cleaned.csv
    
Reports related to the cleaning process are located at:
    ../../data/cleaning_reports/...

"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
from ast import literal_eval

#!!! ATTENTION !!!#
#Pandas does not preserve list structure when saving data to a .csv file.
#Because of this, we need to re-create the column "tagged_sentence" using
# literal_eval.
# More information about literal_eval can be found here:
# https://docs.python.org/3/library/ast.html

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/raw/tagged_sentences_raw.csv")
tagged_sentences = pd.read_csv(import_fp, encoding = "utf-8")
tagged_sentences["tagged_sentence"] = tagged_sentences["tagged_sentence"].apply(literal_eval)

#%% --- Cleaning: filter, document and drop null values ---

#Create masks for null values and non-null values
null_values_mask = tagged_sentences["tagged_sentence"].isnull()

# null_values_mask.sum() == 0, so no need to go any further.

#%% --- Cleaning: assure data type agreement between and within columns ---

error_list = []

for column_name in tagged_sentences.columns:
    expected_dtype = type(tagged_sentences[column_name][0])
    value_index = 0
    while value_index < len(tagged_sentences[column_name]):
        actual_dtype = type(tagged_sentences[column_name][value_index])
        if expected_dtype != actual_dtype:
            error_entry = [column_name, value_index, expected_dtype, actual_dtype]
            error_list.append(error_entry)
        value_index += 1
        
# There appears to be no proof of data-type disagreement. Moving on.

#%% --- Export Data ---

export_fp = Path("../../data/cleaned/tagged_sentences_cleaned.csv")
tagged_sentences.to_csv(export_fp, encoding = "utf-8", index = False)
