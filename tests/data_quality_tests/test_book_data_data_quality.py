# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the book_data.xlsx file.
The file can be found at:
    data/external/book_data.xlsx

"""
#%% --- Import required packages ---

import os
import urllib.request
from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/external/book_data.xlsx")
book_data = pd.read_excel(import_fp)

#%% --- Quality test: check if there are any null values ---

class TestNullValues(object):
    def test_total_null_values(self):
        expected = 0
        actual = book_data.isnull().sum().sum()
        error_message = "Dataset contains null values. Expected {} null values, got {}".format(expected,actual)
        assert expected == actual, error_message

#%% --- Quality test: check if http_id and book_id variable is unique for all rows ---

def TestUniquenessOfVariables(object):
    def test_column_uniqueness_http_id(self):
        expected = len(book_data["http_id"])
        actual =  len(book_data["http_id"].unique)
        error_message = "Column http_id contains non-unique values. Expected {} unique values, got {}".format(expected,actual)
        assert expected == actual, error_message
        
    def test_column_uniqueness_book_id(self):
        expected = len(book_data["book_id"])
        actual =  len(book_data["book_id"].unique)
        error_message = "Column book_id contains non-unique values. Expected {} unique values, got {}".format(expected,actual)
        assert expected == actual, error_message

#%% --- Quality test: check if all https are available ---

def TestHttpAvailability(object):
    def test_http_availability_by_pinging(self):
        for http in  book_data["http"]:
            expected = 200
            actual = urllib.request.urlopen(http).getcode()
            error_message = "The following http is not available: {}".format(http)
            assert expected == actual, error_message
            