# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 22:45:18 2021

@author: ejgen

------ What is this file? ------

This script ingests the file modifiers_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/modifiers_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/modifiers_cleaned.csv
    
Reports related to the cleaning process are located at:
    ../../data/cleaning_reports/...
    
"""

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/raw/modifiers_raw.csv")
modifiers = pd.read_csv(import_fp, encoding = "utf-8")


