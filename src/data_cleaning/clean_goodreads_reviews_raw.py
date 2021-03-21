# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This script ingests the file goodreads_reviews_raw.csv in order to format it
according to some pre-determined quality standarts.


This script targets the following file:
    ../../data/raw/goodreads_reviews_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    
Reports related to the cleaning process are located at:
    ../../data/cleaning_reports/...

"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import datetime as dt
import pandas as pd
from langdetect import DetectorFactory, detect
from langdetect.lang_detect_exception import LangDetectException

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
goodreads_reviews = pd.read_csv(import_fp)

#%% --- Cleaning: filter, document and drop null values ---

#Create masks for null values and non-null values
null_values_mask = goodreads_reviews["review"].isnull()
non_null_values_mask = goodreads_reviews["review"].notnull()

# Select null values only and then update original df according to non-null values
null_values_only = goodreads_reviews.loc[null_values_mask,:]
goodreads_reviews = goodreads_reviews.loc[non_null_values_mask,:].reset_index(drop = True)

#%% --- Cleaning: filter, document and drop duplicate comments. ---

review_id_series = pd.Series(name = "review_id",
                             dtype = "object")

for book_id in goodreads_reviews["book_id"].unique().tolist():
    book_id_mask = goodreads_reviews.loc[:,"book_id"] == book_id
    subset_via_book_id_mask = (goodreads_reviews.loc[book_id_mask,:]
                               .drop_duplicates(subset = "reviewer_id",
                                                keep = "first"))
    
    review_id_series = review_id_series.append(subset_via_book_id_mask["review_id"])
    
unique_review_id_mask = goodreads_reviews.loc[:,"review_id"].isin(review_id_series)

duplicate_reviews = (goodreads_reviews.loc[(~unique_review_id_mask),:]
                     .reset_index())
goodreads_reviews = (goodreads_reviews.loc[unique_review_id_mask,:]
                     .reset_index())
    
#%% --- Cleaning: check and correct data type agreement within columns ---

#The reason why we are not doing a vectorized operation here is that we are
#actually looking at the python data type of each entry under each column,
#and not the data type that Pandas reports to us.

error_list = []

for column_name in goodreads_reviews.columns:
    expected_dtype = type(goodreads_reviews[column_name][0])
    value_index = 0
    while value_index < len(goodreads_reviews[column_name]):
        actual_dtype = type(goodreads_reviews[column_name][value_index])
        if expected_dtype != actual_dtype:
            error_entry = [column_name, value_index, expected_dtype, actual_dtype]
            error_list.append(error_entry)
        value_index += 1
        
# There appears to be no proof of data-type disagreement. Moving on.

#%% --- Cleaning: turn date_scraped and review_date into datetime objects ---

goodreads_reviews["date_scraped"] = pd.to_datetime(goodreads_reviews["date_scraped"],
                                                                     format = "%d/%m/%Y")

goodreads_reviews["review_date"] = pd.to_datetime(goodreads_reviews["review_date"],
                                                                     format = "%b %d, %Y")
#%% --- Cleaning: turn date_scraped and review_date into str with a specific format ---

date_columns = ["date_scraped", "review_date"]

for date_column in date_columns:
    goodreads_reviews[date_column] = goodreads_reviews[date_column].dt.strftime("%d/%m/%Y")
    
#%% --- Cleaning: filter, document and drop possible non-english comments ---

DetectorFactory.seed = 0
# This seed is same as the one used in the data quality tests to ensure consistency.

def throwaway_detect_function(rev_str):
    try:
        result = detect(rev_str)
    except:
        result = "not a language"
    return result == "en"
        
non_english_filter = goodreads_reviews["review"].apply(throwaway_detect_function)

non_english_reviews = goodreads_reviews.loc[~non_english_filter,:]
goodreads_reviews = goodreads_reviews.loc[non_english_filter,:].reset_index(drop = True)

#%% --- Cleaning: normalize all reviews to be lowercase_only

goodreads_reviews.loc[:,"review"] = goodreads_reviews.loc[:,"review"].str.lower()
    
#%% --- Export Data ---

export_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
goodreads_reviews.to_csv(export_fp, encoding = "utf-8", index = False)
            
#%% --- Export cleaning documentation - that has been deleted ---

cleaning_documentation = {"goodreads_reviews_raw_null_values": null_values_only,
                          "goodreads_reviews_raw_nonenglish_comments": non_english_reviews,
                          "goodreads_reviews_raw_duplicate_reviews": duplicate_reviews}

for docname, doc in cleaning_documentation.items():
    export_fp = Path(("../../data/cleaning_reports/{}.csv".format(docname)))
    doc.to_csv(export_fp, encoding = "utf-8", index = False)
    
    