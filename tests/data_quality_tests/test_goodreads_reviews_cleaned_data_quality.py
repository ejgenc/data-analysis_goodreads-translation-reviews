# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the goodreads_reviews_cleaned.csv file.
The file can be found at:
    ../../data/cleaned/goodreads_reviews_cleaned.csv

"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
from langdetect import DetectorFactory, detect

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
        dtype_dict = {"date_scraped": "object",
                      "book_id": "object",
                      "review_id": "object",
                      "reviewer_id": "int64",
                      "reviewer_name": "object",
                      "review_date": "object",
                      "rating": "int64",
                      "review": "object"}
        
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message

#%% --- Quality test: check uniqueness of the entries under certain columns ---

class TestUniqueness(object):
    def test_for_duplicate_ids_per_book(self):
        for book_id in test_target["book_id"].unique().tolist():
            book_id_mask = test_target.loc[:,"book_id"] == book_id
            expected = len(test_target.loc[book_id_mask,"reviewer_id"])
            actual = test_target.loc[book_id_mask,"reviewer_id"].nunique()
            error_message = ("Found duplicate reviews in reviews of book id {}. "
                             "Expected {} unique reviews, found {}"
                             .format(book_id, expected, actual))
            assert expected == actual, error_message
            
    def test_if_selected_are_all_unique(self):
        selected_columns = ["review_id"]
        for column in selected_columns:
            expected = len(test_target[column])
            actual =  len(test_target[column].unique())
            error_message = "Column {} contains non-unique values. Expected {} unique values, got {}".format(column, expected,actual)
            assert expected == actual, error_message
            
#%% --- Quality test: check for formatting errors in datetime formatting ---

class TestDatetime(object):
    def test_formatting_errors(self):
        datetime_columns = ["date_scraped", "review_date"]
        expected = True
        for column in datetime_columns:
            selected = test_target[column]
            for datetime in list(selected):
                parts = datetime.split("/")
                month = int(parts[1])
                actual = month <= 12
                error_message = "Found datetime formatting error. Month cannot be bigger than 12, found {}".format(str(month))
                assert expected == actual, error_message
                
          
#%% --- Quality test: check if "review" column only includes English comments ---

class TestReviewLanguage(object):
    DetectorFactory.seed = 0
    def test_if_reviews_are_english(self):
        expected = 1000
        actual = 0
        for review in test_target["review"]:
            try:
                lang = detect(review)
            except:
                lang = "not a language"
            if lang != "en":
                actual += 1
            error_message = "Language detection did not work as intended. Excepted below {} flags, got {}".format(expected,actual)
            assert expected >= actual, error_message

#%% --- Quality test: check if "review" column strings are all lower case ---

class TestStringConventions(object):
    def test_if_reviews_are_lowercase(self):
        expected = len(test_target["review"])
        actual = test_target["review"].str.islower().sum()
        error_message = "Some of the reviews are not exclusively lower case. Expected {} lower case only reviews, got only {}.".format(expected,actual)
        assert expected == actual, error_message
    