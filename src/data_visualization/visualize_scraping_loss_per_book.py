# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 16:42:07 2021

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
            .loc[:,["book_name", "n_initial_reviews",
                    "n_final_reviews", "perc_lost_after_cleaning",
                    "total_rev_length_in_words", "total_rev_length_in_sents"]])

#%% --- Prepare data ---

# Calculate the data that will be used to annotate in/around the plot
mean_loss_percentage = (sum(dataset.loc[:,"perc_lost_after_cleaning"])
                        / len(dataset.loc[:,"perc_lost_after_cleaning"]))

n_final_reviews = sum(dataset.loc[:,"n_final_reviews"])
total_len_in_sents = sum(dataset.loc[:,"total_rev_length_in_sents"])

#%% --- Plot data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create the figure
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (19.20, 10.80),
                     dpi = 100)
    
    ax = fig.add_subplot(1,1,1)
    
    # Plot the data
    ax.scatter(dataset["n_initial_reviews"],
               dataset["n_final_reviews"],
               s = 250,
               marker = "o",
               facecolor = "#525a61ff",
               edgecolor = "black",
               linewidth = 1)
