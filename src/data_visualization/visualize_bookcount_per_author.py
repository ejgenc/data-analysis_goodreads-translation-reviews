# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 15:55:11 2021

@author: ejgen

------ What is this file? ------

This script visualizes how many authors are represented in the corpus with n
book (n being 1, 2, 3, 4, 9). The script produces a dot plot, where dots can
be placed side to side in rows of three. The emergent pattern resembles a
bar chart and that is indeed the intended effect. The resulting plot is
less accurate than a bar chart and the data is visually "distorted." However,
here precision and truthfulness is not as important because the data is rather
minimal.

NOTE: The result requires some editing.

This script targets the following file:
    ../../data/analysis_results/book_level_statistics.csv
    ../../data/analysis_results/total_modifiers_per_unique_modified.csv
    ...
    
    
The resulting raw figures are located at:
    ../../media/figures/raw/visualize_bookcount_per_author/*
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
# faulty_row = dataset.iloc[9,:]["book_id"]
# faulty_row = (faulty_row
#               .split(",")
#               [0:3])
# dataset.iloc[9,:] = faulty_row

# Get how many authors there are with n books 
num_of_authors_with_n_books = (dataset
                             .copy()
                             ["author"]
                             .value_counts()
                             .replace(9,5)
                             .value_counts())

# Get the raw data so that you can transform it to a plottable manner
dataset = (pd.DataFrame((dataset["author"]
                        .value_counts()
                        .reset_index(drop = True)
                        .replace(9,5)))
           .rename({"author": "x"},
                   axis = 1))

dataset["y"] = 0


# Create a mask for every x value
for unique_x in dataset["x"].unique()[2:]:
    x_mask = dataset["x"] == unique_x
    subset = dataset.loc[x_mask,:]
    new_x = []
    new_y = []
    j = 0
    base_y = 0
    
    for x_value in subset["x"].values:
        print(j)
        j += 1
        if j == 1:
            new_x.append(x_value - 0.1)
        elif j == 2:
            new_x.append(x_value)
        elif j == 3:
            new_x.append(x_value + 0.1)
            base_y += 0.12
            j = 0
        new_y.append(base_y)
        
    print(len(new_x))
    print(len(new_y))
    dataset.loc[x_mask, "x"] = new_x
    dataset.loc[x_mask, "y"] = new_y
    
    
#%%

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create the figure
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (19.20, 10.80),
                     dpi = 100)
    
    ax = fig.add_subplot(1,1,1)
    
    # Plot the data
    ax.scatter(dataset["x"],
               dataset["y"],
               s = 250,
               marker = "o",
               facecolor = "#525a61ff",
               edgecolor = "black",
               linewidth = 1)
    
    # --- Spines and Axes ---
    
    # --- set ylim/xlim
    ax.axes.set_xlim(0.5, 5.5)
    ax.axes.set_ylim(-0.10, 3.5)
    
    # --- set spines ---
    ax.spines["left"].set_visible(False)
    
    # --- Ticks and Labels ---
    
    # --- disable ticks on all axes ---
    ax.set_xticks([1,2,3,4,5])
    ax.tick_params(axis = "both",
                   which = "both",
                   bottom = False,
                   top = False,
                   left = False,
                   right = False)
    
    # --- Modify axis labels ---
    ax.set_yticklabels([])
    ax.set_xticklabels(["1","2","3","4","9"],
                       fontsize = 20,
                       fontweight = "bold")

    # --- Text and annotation ---
    # Set ax title
    ax.set_title(label = "Number of authors who have...",
                 fontsize = 30,
                 fontweight = "bold",
                 loc = "left",
                 pad = 10.0)
                
#%% --- Export data ---

# Prepare directory structure
current_filename_split = os.path.basename(__file__).split(".")[0].split("_")
current_filename_complete = "_".join(current_filename_split)

mkdir_path = Path("../../media/figures/raw/{}".format(current_filename_complete))
os.mkdir(mkdir_path)

# Export data
file_extensions = [".png", ".svg"]
for file_extension in file_extensions:
    filename_extended = "bookcount_per_author" + file_extension
    export_fp = Path.joinpath(mkdir_path, filename_extended)
    fig.savefig(export_fp,
                dpi = 100,
                bbox_inches = "tight",
                pad_inches = 0.2)