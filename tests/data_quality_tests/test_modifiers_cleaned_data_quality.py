# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 21:20:24 2021

@author: ejgen

------ What is this file? ------

This test module contains some data quality tests for the
modifiers_cleaned.csv file.

The file can be found at:
    ../../data/cleaned/modifiers_cleaned.csv
    
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

import_fp = Path("../../data/cleaned/modifiers_cleaned.csv")
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
                    "token_id": "object",
                    "modifier_id":"object",
                    "modifier":"object",
                    "modified":"object",
                    "dependency_relation":"object"
                    }
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message
            
            
#%% --- Quality test: check values for specific columns ---

class TestValues(object):
    def test_for_false_positive_language_modifiers(self):
        languages_list = ["chinese","spanish","english","hindi","bengali",
                  "portuguese","russian","japanese","turkish","korean",
                  "french","german","vietnamese","urdu","italian","arabic",
                  "persian","polish","romanian","dutch","greek","hungarian",
                  "czech","finnish","irish","norwegian","swedish","danish",
                  "lithuanian","latvian","estonian","georgian","armenian",
                  "azerbaijani"]
        language_modifiers_count = test_target["modifier"].isin(languages_list).sum()
        expected = 0
        actual = language_modifiers_count
        error_message = ("Column 'modifier' includes modifiers that denote language.",
                         " expected {} language modifiers, got {}".format(expected,actual))
        assert expected == actual, error_message
    
    def test_for_modified_variation(self):
        acceptable_modified_forms = ["translation", "translations",
                              "translation's", "translations'",
                              "translator", "translators",
                              "translator's", "translators'",
                              "style", "styles","style's", "styles'",
                              "book", "books", "book's", "books'",
                              "author", "authors", "author's", "authors'",
                              "writer", "writers", "writer's", "writers'",
                              "writing", "writings", "writing's", "writings'",
                              "translate", "translates", "translated",
                              "translating", "write", "writes", "wrote",
                              "written"]
        unacceptable_modifiers_count = (~(test_target["modified"].isin(acceptable_modified_forms))).sum()
        expected = 0
        actual = unacceptable_modifiers_count
        error_message = ("Column 'modified' includes modifieds that fall",
                         " outside the expected modified forms.",
                         " Expected {} unfitting modified forms, got {}".format(expected,actual))
        assert expected == actual, error_message
