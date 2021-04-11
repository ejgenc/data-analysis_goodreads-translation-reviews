# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 15:05:50 2021

@author: ejgen

This test module contains some data quality tests for the
goodreads_reviews_analyzed.csv file. the file can be found at:
    ../../data/analysis_results/book_level_statistics.csv
    
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

import_fp = Path("../../data/analysis_results/book_level_statistics.csv")
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
        dtype_dict = {"book_id": "object",
                      "book_name": "object",
                      "author": "object",
                      "n_initial_reviews": "int64",
                      "n_final_reviews": "int64",
                      "perc_lost_after_cleaning": "float64",
                      "total_rev_length_in_words": "int64",
                      "total_rev_length_in_sents": "int64",
                      "mean_rev_length_in_words": "float64",
                      "mean_rev_length_in_sents": "float64",
                      "share_of_only_trans_mentions": "float64",
                      "share_of_trans_mentions": "float64",
                      "share_of_only_orig_mentions": "float64",
                      "share_of_orig_mentions": "float64"}
        
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message

#%% --- Quality test: test the validity of certain values

class TestValueValidity(object):
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
