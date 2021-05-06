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
    
# Calculate summary statistics for each dataset

rows = []

for key, dataset in datasets.items():
    
    total_modifiers = dataset["count"].sum()
    
    row = [key, total_modifiers]
    
    valence_ratios = [1, 0, -1]
    grouped = dataset.groupby("valence")
    for valence in valence_ratios:
        try:
            num = (grouped
                     .get_group(valence)
                     ["count"]
                     .sum())
            ratio = num / total_modifiers
        
            row.append(num)
            row.append(ratio)
        except:
            pass
    
    rows.append(row)
    
summary_stats = (pd.DataFrame(rows,
                             columns = ["dataset_name",
                                        "total_modifiers",
                                        "pos",
                                        "pos_ratio",
                                        "neut",
                                        "neut_ratio",
                                        "neg",
                                        "neg_ratio"])
                 .fillna(0, axis = 1))
    
# Create a color and hatching dict    
color_and_hatching = {"pos": ("#125aa1ff", "/"),
                      "neut": ("#525a61ff","|"),
                      "neg": ("#a03912ff","\\")}

#%% --- Visualize Data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create figure and axes
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (19.20, 10.80),
                     dpi = 100)
    
    ax = fig.add_subplot(1,1,1)
    
    # --- Plot the main bars ---
    
        # --- Cast numerical values to visual marks ---
    main_bar_heights = summary_stats["total_modifiers"].values
    bar_labels = summary_stats["dataset_name"].values
    bar_positions = [2, 3.5, 6.5, 8, 12, 13.5]
    
        # --- Plot data ---
    ax.bar(x = bar_positions,
       height = main_bar_heights,
       align = "center",
       width = 1,
       color = "white",
       edgecolor = "black",
       linewidth = 2)
    
        # --- Axis parameters ---
    ax.axes.set_ylim(0, max(main_bar_heights))
        
        # --- Ticks and labels ---

    # X-ticks
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels,
                       va = "top",
                       ha = "center",
                       fontweight = "bold")
    
    # Remove the ticks but keep the labels
    # NOTE: this has to be done after the fact.
    ax.tick_params(axis = "x",
                   which = "both",
                   bottom = False)
    
    # Y- ticks
    ax.set_yticks([0, max(main_bar_heights) * 0.50, max(main_bar_heights)])

    
    # --- Plot the other bars ---
    valences = ["pos", "neut", "neg"]
    for i,column_name in enumerate(valences):
        bar_heights = summary_stats[column_name].values
        bar_positions = [2, 3.5, 6.5, 8, 12, 13.5]
        
        ax.bar(x = bar_positions,
               height = bar_heights,
                align = "center",
                width = 1,
                color = color_and_hatching[column_name][0],
                hatch = color_and_hatching[column_name][1],
                edgecolor = "black",
                linewidth = 2,
                bottom = summary_stats[valences[i - 1]].values if i > 0 else None)
                     

    
    
    
    
    
    

#%% --- Export data ---

# # Prepare directory structure
# current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
# current_filename_complete = "_".join(current_filename_split)

# mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
# os.mkdir(mkdir_path)

# # Export data
# file_extensions = [".png", ".svg"]

# for name, visualization in visualizations.items():
#     for file_extension in file_extensions:
#         filename_extended = name + file_extension
#         export_fp = Path.joinpath(mkdir_path, filename_extended)
#         visualization.savefig(export_fp,
#                               dpi = 100,
#                               bbox_inches = "tight",
#                               pad_inches = 0.2)

