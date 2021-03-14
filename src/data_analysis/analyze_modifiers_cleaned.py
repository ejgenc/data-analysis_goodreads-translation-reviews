# -*- coding: utf-8 -*-
"""
Created on Sun Mar 14 12:40:55 2021

@author: ejgen

------ What is this file? ------

This script ingests the file modifiers_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/cleaned/modifiers_cleaned.csv
    
The resulting csv files are located at:
    CSV FILES HERE
    
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
modifiers_cleaned = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- ---
