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

import numpy as np
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
loss_percentages = dataset.loc[:,"perc_lost_after_cleaning"]
loss_percentages_stats = (loss_percentages
                          .agg(["min", "max",
                                "mean", "median",
                                "std", "skew"]))

n_initial_reviews = sum(dataset.loc[:,"n_initial_reviews"])
n_final_reviews = sum(dataset.loc[:,"n_final_reviews"])
total_len_in_sents = sum(dataset.loc[:,"total_rev_length_in_sents"])
total_len_in_words = sum(dataset.loc[:,"total_rev_length_in_words"])

# Split the data in a way that will allow for differential coloring
# Get the 5 data points with most reviews lost during scraping
most_lost = (dataset
             .sort_values(
                 by = "perc_lost_after_cleaning",
                 axis = 0,
                 ascending = False)
             .head(5))

# Get the 5 data points with least reviews lost during scraping
least_lost = (dataset
             .sort_values(
                 by = "perc_lost_after_cleaning",
                 axis = 0,
                 ascending = True)
             .head(5))

# Get the data points that can be considered outliers
q1 = np.quantile(loss_percentages, 0.25)
q3 = np.quantile(loss_percentages, 0.75)
iqr = q3 - q1
upper_range = q3 + (1.5 * iqr)
lower_range = q1 - (1.5 * iqr)

range_mask = ((dataset.loc[:, "perc_lost_after_cleaning"] > upper_range)
              | (dataset.loc[:, "perc_lost_after_cleaning"] < lower_range))

outliers = dataset.loc[range_mask, :]

# Join most_lost, least_lost and outliers
outliers_and_extremes = (pd
                         .concat([most_lost, least_lost, outliers])
                         .drop_duplicates())
#%% --- Plot data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create the figure
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (19.20, 10.80),
                     dpi = 100)
    
    # Add the grid layout
    gs = fig.add_gridspec(nrows = 2,
                          ncols = 3,
                          figure = fig,
                          hspace = 0.35)
    
    # Place the axes on the grid
    ax_1 = fig.add_subplot(gs[0,0:2])
    ax_2 = fig.add_subplot(gs[1,0:2])
    ax_3 = fig.add_subplot(gs[0:, 2:])
    
    # --- Plot the data ---
        # Scatterplot
        # Plot once for non-colored values
    ax_1.scatter(dataset["n_initial_reviews"],
                dataset["n_final_reviews"],
                s = 400,
                marker = "o",
                facecolor = "#525a61ff",
                edgecolor = "black",
                alpha = 0.5,
                linewidth = 1)
    
        # Plot again for outliers
    ax_1.scatter(outliers["n_initial_reviews"],
                 outliers["n_final_reviews"],
                 s = 400,
                 marker = "o",
                 facecolor = "#e5501aff",
                 edgecolor = "black",
                 linewidth = 1,
                 hatch = "\\\\")
    
        # Histogram
        # Plot once for non-colored values
    ax_2.hist(loss_percentages,
              bins = 25,
              histtype = "bar",
              facecolor = "#525a61ff",
              edgecolor = "black",
              linewidth = 1)
    
        # Plot again for outliers
    ax_2.hist(outliers["perc_lost_after_cleaning"],
              bins = 25,
              histtype = "bar",
              facecolor = "#e5501aff",
              edgecolor = "black",
              linewidth = 1,
              hatch = "\\\\")
    
    # --- Spines and Axes---
    ax_1.axes.set_xlim(265, 335)
    ax_1.axes.set_ylim(215, 305)
    
    ax_2.axes.set_ylim(0, 33.6)
    
    ax_3.spines["left"].set_visible(False)
    ax_3.spines["bottom"].set_visible(False)
    
    # --- Ticks and Labels ---
    ax_1.set_xticks([270, 280, 290, 300, 310, 320, 330])
    ax_1.set_yticks([220, 240, 260, 280, 300])
    
    ax_2.set_yticks([0, 7.5, 15, 22.5, 30])
    
    ax_3.set_xticks([])
    ax_3.set_yticks([])
    ax_3.tick_params(axis = "both",
                   which = "both",
                   bottom = False,
                   top = False,
                   left = False,
                   right = False)
    
    # --- Text and annotation ---
    ax_1.set_xlabel("Number of reviews initially scraped",
                    fontsize = 14,
                    fontweight = "bold",
                    labelpad = 10)
    
    ax_1.set_ylabel("Number of reviews left after cleaning",
                    fontsize = 14,
                    fontweight = "bold",
                    labelpad = 10)
    
    ax_2.set_xlabel("Count",
                    fontsize = 14,
                    fontweight = "bold",
                    labelpad = 10)
    
    ax_2.set_ylabel("Loss percentage",
                fontsize = 14,
                fontweight = "bold",
                labelpad = 10)
    
    
    ax_1.set_title(label = "Number of reviews before and after cleaning",
                   fontsize = 16,
                   fontweight = "bold",
                   loc = "center",
                   pad = 10.0)
    
    ax_2.set_title(label = "Distribution of loss percentages",
               fontsize = 16,
               fontweight = "bold",
               loc = "center",
               pad = 10.0)
    
    fig.suptitle("Number of reviews in the dataset",
                 fontsize = 18,
                 fontweight = "bold")
    
    # Annotate summary statistics
    # PLACEHOLDER ONLY
    ax_2.text(x = 0,
            y = 0.50,
            s = ["min", "max", "mean", "median", "std", "skew"],
            transform = ax_2.transAxes,
            fontsize = 12)
    
    ax_2.text(x = 0,
        y = 1,
        s = " ".join(str(i) for i in loss_percentages_stats.values),
        transform = ax_2.transAxes,
        fontsize = 12)

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