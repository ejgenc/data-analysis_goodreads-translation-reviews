# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 14:49:32 2020

@author: ejgen

------ What is this file? ------

This test module contains some data quality tests for the
tokens_and_dependencies_cleaned.csv file.

The file can be found at:
    ../../data/cleaned/tokens_and_dependencies_cleaned.csv
    
"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd
import difflib # For string similarity calculation

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/tokens_and_dependencies_cleaned.csv")
test_target = pd.read_csv(import_fp)

#Import reference data
import_fp = Path("../../data/cleaned/review_sentences_cleaned.csv")
reference_data = pd.read_csv(import_fp,
                             usecols = ["sentence_id",
                                        "review_sentence"],
                             index_col = "sentence_id")

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
                    "sent_mentions_original": "bool",
                    "sent_mentions_trans": "bool",
                    "token": "object",
                    "dependency_relation": "object",
                    "parent_token": "object"}
        for column, dtype in dtype_dict.items():
            expected = dtype
            actual = str(test_target[column].dtype)
            error_message = "Column {} is of wrong data type. Expected {}, got {}".format(column, expected, actual)
            assert expected == actual, error_message
            
            
#%% --- Quality test: re-construct sentences by sentence id and check data similarity ---

@pytest.mark.skip(reason="This might be an unnecessary test.")
class TestSentenceLoss(object):
    def test_sentence_loss_by_reconstruction(self):
        #Prepare the necessary data
        test_target_subset = test_target.loc[:,["sentence_id","token"]]
        reconstructed_sentences = test_target_subset.groupby("sentence_id")["token"].agg(list)
        reconstructed_sentences = reconstructed_sentences.str.join("")
        reference_sentences = reference_data.copy()
        reference_sentences = reference_sentences["review_sentence"].str.replace(" ", "")
        sentences_df = pd.concat([reference_sentences,reconstructed_sentences],
                                 axis = 1)
        
        #Do the calculations
        diff_ratio_list = []
        for row in sentences_df.iterrows():
            diff_ratio = difflib.SequenceMatcher(None,
                                                 row[1][0],
                                                 row[1][1]).ratio()
            diff_ratio_list.append(diff_ratio)
            
        # Do the testing
        actual = min(diff_ratio_list)
        expected_limit = 0.95
        error_message = ("Similarity in between at least one original sentence and reconstructed sentence"
                         "is below the limit. Expected {} percent, got {}").format(expected_limit, actual)
        assert actual >= expected_limit, error_message
    