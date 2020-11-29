# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the goodreads_reviews_cleaned.csv file.
The file can be found at:
    data/cleaned/goodreads_reviews_cleaned.csv

"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import datetime as dt
import pytest
import pandas as pd
from langdetect import DetectorFactory, detect
from langdetect.lang_detect_exception import LangDetectException

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
test_target = pd.read_csv(import_fp)

#%% --- Quality test: check if there are any null values ---

class TestNullValues(object):
    def test_total_null_values(self):
        expected = 0
        actual = test_target.isnull().sum().sum()
        error_message = "Dataset contains null values. Expected {} null values, got {}".format(expected,actual)
        assert expected == actual, error_message
        
#%% --- Quality test: check data type agreements within columns and data types

class TestDataTypes(object):
    def test_data_type_agreement_within_columns(self):
        for column_name in test_target.columns:
            expected_dtype = type(test_target[column_name][0])
            value_index = 0
            while value_index < len(test_target[column_name]):
                value_type = type(test_target[column_name][value_index])
                error_message = "Values in column \"{}\" are not all of same type. Value at index {} is type {}, expected type {}".format(column_name, value_index, value_type, expected_dtype)
                assert value_type == expected_dtype, error_message
                value_index += 1
                
    def test_if_selected_columns_are_of_correct_dtype(self):
        dtype_dict = {"date_scraped": "datetime64[ns]",
                      "book_id": "object",
                      "review_id": "object",
                      "reviewer_id": "int64",
                      "reviewer_name": "object",
                      "review_date": "datetime64[ns]",
                      "rating": "int64",
                      "review": "object"}
        
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message

#%% --- Quality test: check uniqueness of the entries under certain columns ---

class TestUniqueness(object):
    def test_if_selected_are_all_unique(self):
        selected_columns = ["review_id"]
        for column in selected_columns:
            expected = len(test_target[column])
            actual =  len(test_target[column].unique())
            error_message = "Column {} contains non-unique values. Expected {} unique values, got {}".format(column, expected,actual)
            assert expected == actual, error_message
              
#%% --- Quality test: check if "review" column only includes English comments ---

class TestReviewLanguage(object):
    def test_if_reviews_are_english(self):
        DetectorFactory.seed = 1
        expected = "en"
        for review in test_target["review"]:
            try:
                actual = detect(review)
            except:
                actual = "not a language"
            error_message = "Found a non-english review. Language detector returned language code {}, expected {}".format(actual,expected)
            assert expected == actual, error_message
            
#%% --- Quality test: check if "review" column strings are all lower case and contain no stopwords ---

class TestStringConventions(object):
    def test_if_reviews_are_lowercase(self):
        expected = len(test_target["review"])
        actual = test_target["review"].str.islower().sum()
        error_message = "Some of the reviews are not exclusively lower case. Expected {} lower case only reviews, got only {}.".format(expected,actual)
        assert expected == actual, error_message
    



