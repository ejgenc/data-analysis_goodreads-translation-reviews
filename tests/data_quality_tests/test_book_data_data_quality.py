# -*- coding: utf-8 -*-
"""
------ What is this file? ------

This test module contains some data quality tests for the book_data.xlsx file.
The file can be found at:
    data/external/book_data.xlsx

"""
#%% --- Import Required Packages ---

import os
from pathlib import Path # To wrap around filepaths
import pytest
import pandas as pd

