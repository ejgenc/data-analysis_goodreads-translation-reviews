# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the reviews_raw.csv file.
The file can be found at:
    data/raw/reviews_raw.csv

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

import_fp = Path("../../data/raw/reviews_raw.csv")
reviews_raw = pd.read_csv(import_fp)
