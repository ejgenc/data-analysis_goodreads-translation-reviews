# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some tests for the data_preparation_helper_functions.py script.
The script can be found at:
    src/helper_functions/data_preparation_helper_functions.py

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.helper_functions import data_preparation_helper_functions as functions
from numpy import arange

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Create mock tests objects ---

#%% --- Tests for Helper Functions ---

#%% --- Subfunction: read_http_data ---

#%% --- helper_function: df_has_http_column ---

class TestDfHasHttpColumn:



