# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:55:11 2021

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

input_fp = Path("../../data/analysis_results/book_level_statistics.csv")
dataset = (pd
            .read_csv(input_fp, encoding = "utf-8")
            .loc[:,["book_id", "book_name", "author"]])

#%% --- Prepare data ---

# There appears to be a faulty row due to an encoding error on index 9
faulty_row = dataset.iloc[9,:]["book_id"]
faulty_row = (faulty_row
              .split(",")
              [0:3])
dataset.iloc[9,:] = faulty_row

# Get the bookcount per author
bookc_per_author = dataset["author"].value_counts().values

# Get the totals so that you can annotate them
bookcounts = {}
for count in bookc_per_author:
    if count not in bookcounts:
        if count == 9:
            count = 5
        bookcounts[count] = 1
    else:
        bookcounts[count] += 1

# Create a faux dataset so that you can plot in on the scatterplot
# Add 0 to all values
data_to_plot = pd.DataFrame(bookc_per_author,
                            columns = ["x"])
data_to_plot["y"] = [0 for x in bookc_per_author]

#Make "9" into "5"
data_to_plot.loc[0,"x"] = 5

new_x = []

for bookcount, value in bookcounts.items():
    print(bookcount, value)
    if value == 1:
        new_x.append(bookcount)
    if value == 2:
        to_append = [bookcount - 0.2, bookcount]
        new_x += to_append
    if value >= 3:
        counter = 0
            
        
#%% --- Visualize data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create the figure
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (10.80, 10.80),
                     dpi = 100)
    
    # Create the main ax
    ax = fig.add_subplot(1,1,1)
    
    # --- Plot Data ---
    ax.scatter(data_to_plot["x"],
               data_to_plot["y"])
    
    
    # --- Spines and Axes ---
    ax.axes.set_ylim(-0.5,5)
    ax.axes.set_xlim(0.5, 5.5)
    
    
    # while rownum <= 2 and colnum <= 1:
        
    #     ax = fig.add_subplot(gs[rownum, colnum])
        
    #     # --- Cast numerical values to visual marks ---
    #     row = summary_stats.iloc[i]
    #     wedge_sizes = row[["pos","neut","neg"]]
        
    #     # --- Plot data ---
    #     ax.pie(x = wedge_sizes,
    #            labels = wedge_sizes,
    #            colors = colors,
    #            autopct = "%.2f",
    #            startangle = 90,
    #            radius = 1.2,
    #            wedgeprops = {"edgecolor": "black",
    #                          "linewidth": 2})
        
    #     # --- Color and Texture ---
    #     # Since coloring is handled by the .pie() method itself,
    #     # only texture is done here.
    #     for wedge, texture in zip(ax.patches, hatching):
    #         wedge.set(hatch = texture)
             
    
    #     # --- Helpers ---
    #     # Move over the grid 
    #     colnum += 1
    #     if colnum > 1:
    #         colnum = 0
    #         rownum += 1
            
    #     # Select new rows
    #     i += 1
    
    # # --- Text and Annotation ---
    # # Set figure title
    # fig.suptitle(("A comparison of the valence of the top twenty\n"
    #               "modifiers for each comparison group"),
    #       fontsize = 16,
    #       fontweight = "bold",
    #       ha = "right")





            

