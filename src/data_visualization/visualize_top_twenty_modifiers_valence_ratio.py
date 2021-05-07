# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:32:22 2021

@author: ejgen

------ What is this file? ------

This script targets the analysis result data that describes the valence
(positive / neutral / negative) of the top twenty modifiers used to modify
each modifier groups (author/translator etc.) The script produces multiple
pie charts. Each pie chart is divided into 2/3 segments depending on the
valence of the top twenty words that they represent. The color/hatching
of the segment represents a valence category. The size of the segment
represents the amount of the words with the encoded valence.

NOTE: The result requires a substantial amount of editing.

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
            row.append(num)
        except:
            pass
    
    rows.append(row)
    
summary_stats = (pd.DataFrame(rows,
                             columns = ["dataset_name",
                                        "total_modifiers",
                                        "pos",
                                        "neut",
                                        "neg"])
                 .fillna(0, axis = 1))
    
# Create a color and hatching list
colors = ["#125aa1ff", "#525a61ff", "#a03912ff"]
hatching = ["/", "|", "\\"] 


#%% --- Visualize data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create the figure
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (10.80, 10.80),
                     dpi = 100)
    
    # Init a grid spec to orchestrate subplots
    gs = fig.add_gridspec(nrows = 3,
                          ncols = 3,
                          figure = fig,
                          wspace = 0,
                          hspace = 0)
    
    # Init the grid counter
    rownum = 0
    colnum = 0
    
    # Init the row counter
    i = 0
    
    
    while rownum <= 2 and colnum <= 1:
        
        ax = fig.add_subplot(gs[rownum, colnum])
        
        # --- Cast numerical values to visual marks ---
        row = summary_stats.iloc[i]
        wedge_sizes = row[["pos","neut","neg"]]
        
        # --- Plot data ---
        ax.pie(x = wedge_sizes,
               labels = wedge_sizes,
               colors = colors,
               autopct = "%.2f",
               startangle = 90,
               radius = 1.2,
               wedgeprops = {"edgecolor": "black",
                             "linewidth": 2})
        
        # --- Color and Texture ---
        # Since coloring is handled by the .pie() method itself,
        # only texture is done here.
        for wedge, texture in zip(ax.patches, hatching):
            wedge.set(hatch = texture)
             
    
        # --- Helpers ---
        # Move over the grid 
        colnum += 1
        if colnum > 1:
            colnum = 0
            rownum += 1
            
        # Select new rows
        i += 1
    
    # --- Text and Annotation ---
    # Set figure title
    fig.suptitle(("A comparison of the valence of the top twenty\n"
                  "modifiers for each comparison group"),
          fontsize = 16,
          fontweight = "bold",
          ha = "right")


#%% --- Export data ---

# Prepare directory structure
current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

# Export data
file_extensions = [".png", ".svg"]

for file_extension in file_extensions:
    filename_extended = "valence ratios" + file_extension
    export_fp = Path.joinpath(mkdir_path, filename_extended)
    fig.savefig(export_fp,
                dpi = 100,
                bbox_inches = "tight",
                pad_inches = 0.2)

