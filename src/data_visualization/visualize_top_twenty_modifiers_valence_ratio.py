# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:32:22 2021

@author: ejgen

------ What is this file? ------

This script targets the analysis result data that describes the valence
(positive / neutral / negative) of the top twenty modifiers used to modify
each modifier groups (author/translator etc.) The script produces a multiple
stacked bar chart. The height of the bars encode the number of non-unique
modifiers. Each bar is seperated into 3 different zones ("stacks") which represent
the valence of the modifiers. The height of these zones is dependant on the prevalence
of each valence group in their subjective bars. These zones are colored and
given texture according to the valence that they represent.

This script targets the following files:
    ../../data/analysis_results/total_modifiers_per_modified_group.csv
    ../../data/analysis_results/total_modifiers_per_unique_modified.csv
    ...
    
    
The resulting raw figures are located at:
    ../../media/figures/raw/visualize_top_twenty_modifiers_valence_ratio/*
"""

#%% --- Import required packages ---

import os

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

from src.helper_functions.data_visualization_helper_functions import *
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

# Get the top 20 modifiers for each modifier group
datasets = {group: pd.read_csv(filepath).head(20) for group, filepath in filepaths.items()}

#%% --- Prepare Data ---

# Encode valence values
# 1 stands for positive, 0 stands for neutral
# and -1 stands for negative valence values.
valence_values = {"author": [0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0,
                             0, 0, 0, 0, 1, 0, 0, 1, 0],
                  "translator": [0, 0, 0, 1, 1, 1, 1, 0, 1, 0,
                                 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
                  "book": [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
                           1, 0, 1, 1, 0, 1, 0, 0],
                  "translation": [0, 1, 0, 1, 0, -1, 1, -1, -1, 1,
                                   0, 0, 0, 1, 1, 0, 0, 1, 0, 0],
                  "verb_write": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 1, 1, 0, -1, 0, 0, 0, 0],
                  "verb_translate": [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                     0, 0, 1, -1, 0, 0, 0, 0, 0]}

for key, value in valence_values.items():
    datasets[key]["valence"] = value
    
# Encode color and hatching according to valence values
for dataset in datasets.values():
    dataset["color"] = (dataset["valence"].copy()
                        .replace({1: "#125aa1ff",
                                  0: "#525a61ff",
                                  -1: "#a03912ff"}))
    
    dataset["hatching"] = (dataset["valence"].copy()
                           .replace({1: "/",
                                     0: "|",
                                     -1: "\\"}))
#%% --- Visualize Data ---

