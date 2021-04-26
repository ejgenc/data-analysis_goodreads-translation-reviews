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
from numpy import arange
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

# Get the top 20 modifiers for each modifier group
datasets = {group: pd.read_csv(filepath).head(20) for group, filepath in filepaths.items()}

#%% --- Prepare Data ---

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



#%% --- Visualization ---

visualizations = {group: None for group, dataset in datasets.items()}

#%%

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    
    # Create figure and axes
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (19.20, 10.80),
                     dpi = 100)
    
    # Implement a grid-like system
    gs = fig.add_gridspec(nrows = 3,
                          ncols = 2,
                          figure = fig,
                          wspace = 0.30)
    # set the column and row counter to move over grid
    rownum = 0
    colnum = 0
    
    # Keep track of max and min value to set proper axes
    axis_min = 0
    axis_max = 0
    
    for key, data in datasets.items():
        ax = fig.add_subplot(gs[rownum, colnum])
        
        # Cast numerical values to visual marks
        bar_widths = data["count"].values
        bar_labels = data["modifier"].values
        bar_positions = [i * 40 for i in range(0, len(bar_labels))]
        
        # Dynamically update axis max
        if max(bar_widths) > axis_max:
            axis_max = max(bar_widths)
        

        # --- Plot Data ---
        ax.barh(y = bar_positions,
            width = bar_widths,
            align = "center",
            height = 1,
            edgecolor = "black")
        
        # --- Spines and Axes ---

        if colnum == 0:
            # --- set spines ---
            ax.spines["top"].set_visible(True)
            ax.spines["bottom"].set_visible(False)
            ax.spines["right"].set_visible(True)
            ax.spines["left"].set_visible(False)
        
            # --- invert axes for left/top align ---
            ax.invert_xaxis()
            ax.invert_yaxis()
            
            # Set axis length to the max possible value
            ax.axes.set_xlim(axis_max, axis_min)
            ax.axes.set_ylim(20, -20)
        
        if colnum == 1:
            # --- set spines ---
            ax.spines["top"].set_visible(True)
            ax.spines["bottom"].set_visible(False)
            
            # --- invert axes for left/top align ---
            ax.invert_yaxis()
            
        # --- Ticks and Labels ---
        if colnum == 0:
            ax.xaxis.tick_top()
            ax.yaxis.tick_right()
            
            ax.set_yticks(bar_positions)
            
            ax.xaxis.set_label_position('top') 
            ax.yaxis.set_label_position("right")
            
            ax.set_yticklabels(bar_labels)
            
            
        if colnum == 1:
            ax.xaxis.tick_top()
            
            ax.set_yticks(bar_positions)
            
            ax.set_yticklabels(bar_labels)
            
        
        # Move over the grid
        if colnum == 1:
            rownum += 1
            colnum = 0
        else:
            colnum += 1
                    
    for ax in fig.axes:
        ax.set_xticks([axis_min, axis_max])
        


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
#                               dpi = 100,
#                               bbox_inches = "tight",
#                                pad_inches = 0)


#%% 
    
# Create figure and axes
# Figsize calculation in pixels is figsizex/y * dpi
fig = plt.figure()

ax = fig.add_subplot(1, 1, 1)

# Cast numerical values to visual marks
bar_heights = data["count"].values
bar_labels = data["modifier"].values
bar_positions = [i * 5 for i in range(0, len(bar_labels))]



# --- Plot Data ---
ax.bar(x = bar_positions,
    height = bar_heights,
    align = "center",
    width = 3,
    edgecolor = "black")

ax.axes.set_xlim(0, 60)

#     # --- Spines and Axes ---

#     if colnum == 0:
#         # --- set spines ---
#         ax.spines["top"].set_visible(True)
#         ax.spines["bottom"].set_visible(False)
#         ax.spines["right"].set_visible(True)
#         ax.spines["left"].set_visible(False)

#         # --- invert axes for left/top align ---
#         ax.invert_xaxis()
#         ax.invert_yaxis()
    
#         # Set axis length to the max possible value
#         ax.axes.set_xlim(axis_max, axis_min)

#     if colnum == 1:
#         # --- set spines ---
#         ax.spines["top"].set_visible(True)
#         ax.spines["bottom"].set_visible(False)
    
#         # --- invert axes for left/top align ---
#         ax.invert_yaxis()
    
#     # --- Ticks and Labels ---
#     if colnum == 0:
#         ax.xaxis.tick_top()
#         ax.yaxis.tick_right()
    
#         ax.set_yticks(bar_positions)
    
#         ax.xaxis.set_label_position('top') 
#         ax.yaxis.set_label_position("right")
    
#         ax.set_yticklabels(bar_labels)
    
    
#     if colnum == 1:
#         ax.xaxis.tick_top()
    
#         ax.set_yticks(bar_positions)
    
#         ax.set_yticklabels(bar_labels)
    

#     # Move over the grid
#     if colnum == 1:
#         rownum += 1
#         colnum = 0
#     else:
#         colnum += 1
            
# for ax in fig.axes:
#     ax.set_xticks([axis_min, axis_max])
    





