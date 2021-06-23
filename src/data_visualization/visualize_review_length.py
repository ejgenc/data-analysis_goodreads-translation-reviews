# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 14:37:08 2021

@author: ejgen

------ What is this file? ------

This script ...
NOTE: The result requires ....

This script targets the following file:
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
    
The resulting raw figures are located at:
    ../../media/figures/raw/visualize_review_length/*
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

input_fp = Path("../../data/analysis_results/goodreads_reviews_analyzed.csv")
dataset = (pd
           .read_csv(input_fp, encoding = "utf-8")
           .loc[:,["total_length_in_words", "total_length_in_sentences"]])

#%% --- Prepare data ---

len_in_sents_stats = (dataset.loc[:,"total_length_in_sentences"]
                      .agg(["min", "max",
                            "mean", "median",
                            "std", "skew"]))


len_in_words_stats = (dataset.loc[:,"total_length_in_words"]
                      .agg(["min", "max",
                            "mean", "median",
                            "std", "skew"]))
#%% --- Plot data ---

with plt.style.context('matplotlib_stylesheet_ejg_fixes'):
    # --- Visualization setup ---
        
    # Create the figure
    # Figsize calculation in pixels is figsizex/y * dpi
    fig = plt.figure(figsize = (19.20, 10.80),
                     dpi = 100)
    
    # Add the grid layout
    gs = fig.add_gridspec(nrows = 2,
                          ncols = 2,
                          figure = fig,
                          hspace = 0.35)
    
    # Place the axes on the grid
    ax_1 = fig.add_subplot(gs[0,0])
    ax_2 = fig.add_subplot(gs[0,1])
    ax_3 = fig.add_subplot(gs[1,0])
    ax_4 = fig.add_subplot(gs[1,1])
    
    
    # --- Plot the data ---
    ax_1.hist(dataset["total_length_in_sentences"],
              bins = 50,
              histtype = "bar",
              facecolor = "#525a61ff",
              edgecolor = "black",
              linewidth = 1)
    
    ax_2.hist(np.log10(dataset["total_length_in_sentences"]),
          bins = 20,
          histtype = "bar",
          facecolor = "#525a61ff",
          edgecolor = "black",
          linewidth = 1)
    
    ax_3.hist(dataset["total_length_in_words"],
              bins = 50,
              histtype = "bar",
              facecolor = "#525a61ff",
              edgecolor = "black",
              linewidth = 1)
    
    ax_4.hist(np.log10(dataset["total_length_in_words"]),
          bins = 50,
          histtype = "bar",
          facecolor = "#525a61ff",
          edgecolor = "black",
          linewidth = 1)
    
    # --- Text and annotation ---
    ax_1.set_xlabel("Length in sentences",
                    fontsize = 14,
                    fontweight = "bold",
                    labelpad = 10)
    
    ax_2.set_xlabel("Length in sentences (log10)",
                fontsize = 14,
                fontweight = "bold",
                labelpad = 10)
    
    ax_3.set_xlabel("Length in words",
                fontsize = 14,
                fontweight = "bold",
                labelpad = 10)
    
    ax_4.set_xlabel("Length in words (log10)",
            fontsize = 14,
            fontweight = "bold",
            labelpad = 10)
    
    for ax in fig.get_axes():
        ax.set_ylabel("Count",
                      fontsize = 14,
                      fontweight = "bold",
                      labelpad = 10)
    
    fig.suptitle("Distribution of review length in sentences and words",
             fontsize = 20,
             y = 1.02,
             fontweight = "bold")
    
    # Annotate summary statistics
    # PLACEHOLDER ONLY
    
    ax_1.text(x = 0,
              y = 0.50,
              s = list(len_in_sents_stats.index),
              transform = ax_1.transAxes,
              fontsize = 12)
    
    ax_1.text(x = 0,
          y = 0.25,
          s = " ".join(str(i) for i in len_in_sents_stats.values),
          transform = ax_1.transAxes,
          fontsize = 12)
    
    ax_3.text(x = 0,
          y = 0.50,
          s = list(len_in_words_stats.index),
          transform = ax_3.transAxes,
          fontsize = 12)
    
    ax_3.text(x = 0,
          y = 0.25,
          s = " ".join(str(i) for i in len_in_words_stats.values),
          transform = ax_3.transAxes,
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
    filename_extended = "review_length" + file_extension
    export_fp = Path.joinpath(mkdir_path, filename_extended)
    fig.savefig(export_fp,
                dpi = 100,
                bbox_inches = "tight",
                pad_inches = 0.2)