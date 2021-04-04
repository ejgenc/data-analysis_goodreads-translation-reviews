# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:54:18 2021

@author: ejgen

This test module contains some data quality tests for the
goodreads_reviews_analyzed.csv file. the file can be found at:
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
    
"""
#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/analysis_results/goodreads_reviews_analyzed.csv")
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
                      "review": "object",
                      "total_length_in_words": "int64",
                      "total_length_in_sentences": "int64",
                      "share_of_only_trans_mentions": "float64",
                      "share_of_trans_mentions": "float64",
                      "share_of_only_orig_mentions": "float64",
                      "share_of_orig_mentions": "float64",
                      "avg_VADER_score": "float64"}
        
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
            expected = test_target.loc[book_id_mask,"reviewer_id"].nunique()
            actual = len(test_target.loc[book_id_mask,"reviewer_id"])
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
            
#%% --- Quality test: test the validity of certain values

class TestValueValidity(object):
    def test_validity_of_VADER_scores(self):
        expected = len(test_target["avg_VADER_score"])
        actual = ((-1 <= test_target["avg_VADER_score"]) & (1 >= test_target["avg_VADER_score"])).sum()
        error_message = "Column avg_VADER_score contains scores outside of the expected range."
        assert expected == actual, error_message
    
    def test_validity_of_mention_percentages(self):
        expected = len(test_target["share_of_orig_mentions"])
        pairs = [("share_of_only_trans_mentions","share_of_only_orig_mentions"),
                 ("share_of_only_trans_mentions", "share_of_orig_mentions"),
                 ("share_of_trans_mentions", "share_of_only_orig_mentions")]
        for pair in pairs:
            summed = (test_target[pair[0]] + test_target[pair[1]])
            actual = ((summed >= 0) & (summed <= 100)).sum()
            error_message = "Mention percentages are not within the expected range."
            assert expected == actual, error_message
