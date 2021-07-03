# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the book_data_external.xlsx file.
The file can be found at:
    data/external/book_data_external.xlsx

"""
#%% --- Import required packages ---

import os
import requests
from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/external/book_data_external.xlsx")
test_target = pd.read_excel(import_fp, engine="openpyxl")

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
                
#%% --- Quality test: check uniqueness of  the entries under certain columns ---

class TestUniqueness(object):
    def test_if_selected_are_all_unique(self):
        selected_columns = ["http_id","book_id"]
        for column in selected_columns:
            expected = len(test_target[column])
            actual =  len(test_target[column].unique())
            error_message = "Column {} contains non-unique values. Expected {} unique values, got {}".format(column, expected,actual)
            assert expected == actual, error_message
            
    def test_if_selected_columns_are_of_correct_dtype(self):
        dtype_dict = {"http_id": "object",
                      "http": "object",
                      "book_id": "object",
                      "book_name": "object",
                      "author": "object"}
        
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message
