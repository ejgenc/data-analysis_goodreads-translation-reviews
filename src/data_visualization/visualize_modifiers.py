# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 14:33:47 2021

@author: ejgen

------ What is this file? ------

This script targets the analysis result data that describes which 
unique modifiers have been used for which modified groups (author/translator etc.)
how many times. The script produces a horizontal bar chart for each
modified group. The number of occurence of each unique modifier is encoded
by using position on a common scale(y-axis) / bar length. The same information
is reduntantly encoded with textual annotation. Categorical information about
modifier classification (positive - neutral - negative) is encoded using color
hue. The said hue is applied on both the variables names, the data markers
and textual annotation. Summary statistics is presented in text.

This script targets the following files:
    ../../data/analysis_results/total_modifiers_per_modified_group.csv
    ../../data/analysis_results/total_modifiers_per_unique_modified.csv
    ...
    
    
The resulting raw figures are located at:
    ../../media/figures/raw/visualize_modifiers/*
"""

#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import pandas as pd
import matplotlib.pyplot as plt

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

filepaths = {"author": Path("../../data/analysis_results/"
                 "group_refers_to_author_modifier_value_counts.csv"),
             "translator": Path("../../data/analysis_results/"
                 "group_refers_to_translator_modifier_value_counts.csv"),
             "book": Path("../../data/analysis_results/"
                 "group_refers_to_book_modifier_value_counts.csv"),
             "translation": Path("../../data/analysis_results/"
                 "group_refers_to_translation_modifier_value_counts.csv"),
             "verb_write": Path("../../data/analysis_results/"
                 "group_refers_to_vwriting_modifier_value_counts.csv"),
             "verb_translate": Path("../../data/analysis_results/"
                 "group_refers_to_vtranslation_modifier_value_counts.csv")}

datasets = {group: pd.read_csv(filepath) for group, filepath in filepaths.items()}

#%% --- Visualization ---

visualizations = {group: None for group, dataset in datasets.items()}

#%%

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    fig = plt.figure(figsize = (5, 5))
    ax_1 = fig.add_subplot(1, 1, 1)


#%% --- Export data ---

# Prepare directory structure
current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

# Export data
# file_extensions = [".png", ".svg"]

# for name, visualization in visualizations.items():
#     for file_extension in file_extensions:
#         filename_extended = name + file_extension
#         export_fp = Path.joinpath(mkdir_path, filename_extended)
#         visualization.savefig(export_fp,
#                               bbox_inches = "tight")




