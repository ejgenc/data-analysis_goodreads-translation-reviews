# -*- coding: utf-8 -*-
"""
------ What is this file? ------
This script targets the all the intermediary and final data output produced by the data analysis pipeline.
It fits into the start of the pipeline as a measure to assure a clean run of the analysis.
"""
#%% --- Import Required Packages ---

import os
import shutil
from pathlib import Path # To wrap around filepaths

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Process folder names and delete paths ---

folder_names = ["raw","cleaned","analysis_results","cleaning_reports"]
folder_prefix = "../../data/{}"

for folder_name in folder_names:
    folder_path = Path(folder_prefix.format(folder_name))
    for filename in os.listdir(folder_path):
        if filename != ".gitkeep" or filename != "goodreads_reviews_raw.csv":
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))