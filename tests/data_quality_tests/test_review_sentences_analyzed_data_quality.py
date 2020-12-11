# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 15:02:23 2020

@author: ejgen

This test module contains some data quality tests for the review_sentences_analyzed.csv file.
The file can be found at:
    ../../data/analysis_results/review_sentences_analyzed.csv

"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/analysis_results/review_sentences_analyzed.csv")
test_target = pd.read_csv(import_fp)

#%% --- Quality test: check if there are any null values ---

class TestNullValues(object):
    def test_total_null_values(self):
        expected = 0
        actual = test_target.isnull().sum().sum()
        error_message = "Dataset contains null values. Expected {} null values, got {}".format(expected,actual)
        assert expected == actual, error_message

#%% --- Quality test: check data type agreements within columns and data types ---

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
        dtype_dict = {
                    "book_id": "object",
                    "review_id": "object",
                    "sentence_id": "object",
                    "review_sentence": "object",
                    "length_in_words": "int64",
                    "mentions_trans": "bool",
                    "VADER_score_neg": "float64",
                    "VADER_score_neu": "float64",
                    "VADER_score_pos": "float64",
                    "VADER_score_compound": "float64"}
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message

#%% --- Quality test: check if "length_in_words_with_stopwords" column is >= 3 ---

class TestValueBoundaries(object):
    def test_minimum_value_of_selected_columns(self):
        min_value_dict = {
            "length_in_words": 3}
        for column, min_value in min_value_dict.items():
            expected_threshold = min_value
            actual = test_target[column].min()
            error_message = ("Minimum value of column {} is below the threshold of {}."
                             "got at least one row with value {}").format(column,expected_threshold,actual)
            assert expected_threshold <= actual, error_message
