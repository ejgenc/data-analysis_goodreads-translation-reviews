# -*- coding: utf-8 -*-
"""
Created on Wed Dec 2 23:24:42 2020
@author: ejgen

------ What is this file? ------

This script ingests the file review_sentences_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/review_sentences_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/review_sentences_cleaned.csv
    
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

import_fp = Path("../../data/raw/review_sentences_raw.csv")
review_sentences = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Cleaning: filter, document and drop null values ---

#Create masks for null values and non-null values
null_values_mask = review_sentences["review_sentence"].isnull()

# null_values_mask.sum() == 0, so no need to go any further.

#%% --- Cleaning: assure data type agreement between and within columns ---

error_list = []

for column_name in review_sentences.columns:
    expected_dtype = type(review_sentences[column_name][0])
    value_index = 0
    while value_index < len(review_sentences[column_name]):
        actual_dtype = type(review_sentences[column_name][value_index])
        if expected_dtype != actual_dtype:
            error_entry = [column_name, value_index, expected_dtype, actual_dtype]
            error_list.append(error_entry)
        value_index += 1
        
# There appears to be no proof of data-type disagreement. Moving on.

#%% --- Cleaning: drop rows whose review sentences is shorter than 3 words. ---

# Create a boolean mask that flags review sentences shorter than 3
shorter_than_3_mask = (review_sentences["review_sentence"].str.split(" ").str.len()) < 3

# Select those sentences as a subset for documentation
shorter_than_3 = review_sentences.loc[shorter_than_3_mask,:]

# Get the element-wise logical NOT of the mask
reverse_mask = ~shorter_than_3_mask

# Drop based on the reverse mask.
review_sentences = review_sentences.loc[reverse_mask,:].reset_index(drop = True)

#%% --- Export Data ---

export_fp = Path("../../data/cleaned/review_sentences_cleaned.csv")
review_sentences.to_csv(export_fp, encoding = "utf-8", index = False)
            
#%% --- Export cleaning documentation ---

export_fp = Path("../../data/cleaning_reports/review_sentences_raw_shorter_than_three_words.csv")
shorter_than_3.to_csv(export_fp, encoding = "utf-8", index = False)

