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
import matplotlib.pyplot as 

from src.helper_functions import data_visualization_helper_functions as viz_helper
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

visualizations = {"author/translator": None,
                  "book/translation": None,
                  "vwrite/vtranslate": None}
 
#%% --- 

#Since we will be creating three plots with two axes according 
# to visualizations dict,we need to create 3 subsets of the datasets
# of size 2
start, end = 0, 2
i = 0

while end <= 6:
    with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
        
        # --- Visualization Setup ---
        
        # Create figure and axes
        # Figsize calculation in pixels is figsizex/y * dpi
        fig = plt.figure(figsize = (19.20, 10.80),
                         dpi = 100)
        
        # Implement a grid-like system
        gs = fig.add_gridspec(nrows = 1,
                              ncols = 2,
                              figure = fig,
                              wspace = 0.35)
        
        # set the column and row counter to move over grid
        colnum = 0
        
        # Keep track of max and min value to set proper axes
        axis_min = 0
        axis_max = 0
        
        for data in list(datasets.values())[start:end]:
            ax = fig.add_subplot(gs[0, colnum])
            
            # --- Get data ---
            
            # Cast numerical values to visual marks
            bar_widths = data["count"].values
            bar_labels = data["modifier"].values
            bar_positions = [i for i in range(0, len(bar_labels))]
            
            # Calculate summary statistics
            num_of_modifiers = data["count"].sum()
            pos_count = sum(data["valence"] == 1)
            neut_count = sum(data["valence"] == 0)
            neg_count = sum(data["valence"] == -1)
            
            
            # Dynamically update the length of axes
            # In each plot, the length of the x-axis of each chart
            # is equal to the highest value
            if max(bar_widths) > axis_max:
                axis_max = max(bar_widths)
            
    
            # --- Plot data ---
            ax.barh(y = bar_positions,
                width = bar_widths,
                align = "center",
                height = 0.75,
                edgecolor = "black",
                linewidth = 2)
            
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
            
            if colnum == 1:
                # --- set spines ---
                ax.spines["top"].set_visible(True)
                ax.spines["bottom"].set_visible(False)
                
                # --- invert axes for left/top align ---
                ax.invert_yaxis()
                
                # Set axis length to the max possible value
                ax.axes.set_xlim(axis_min, axis_max)
            
            # Set where the bars will start
            ax.axes.set_ylim(20, -0.75)
                
            # --- Ticks and Labels ---
            if colnum == 0:
                ax.xaxis.tick_top()
                ax.yaxis.tick_right()
                
                ax.set_yticks(bar_positions)
                
                ax.xaxis.set_label_position('top') 
                ax.yaxis.set_label_position("right")
                
                
                ax.set_yticklabels(bar_labels,
                                   ha = "left")
            
                
            if colnum == 1:
                ax.xaxis.tick_top()
                
                ax.set_yticks(bar_positions)
                
                ax.set_yticklabels(bar_labels,
                                   # color = red ATTENTION, HOW YOU WILL COLOR IT
                                   ha = "right")
            
            # Disable axis ticks for y axis on both bar charts
            ax.tick_params(axis = "y",
               which = "both",
               bottom = False,
               top = False,
               left = False,
               right = False)
                
            
            # Move over the grid
            colnum += 1
                        
        # Set xticks dynamically to 0 - max/2 - max
        for ax in fig.axes:
            ax.set_xticks([axis_min, round(axis_max / 2), axis_max])
          
    # --- Visualization Teardown ---
    visualizations[list(visualizations.keys())[i]] = fig
    i += 1
    start, end = end, end + 2

#%% --- Export data ---

# Prepare directory structure
# current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
# current_filename_complete = "_".join(current_filename_split)

# mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
# os.mkdir(mkdir_path)

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

