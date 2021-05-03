# -*- coding: utf-8 -*-
"""
Created on Mon May  3 18:14:17 2021

@author: ejgen
"""

#%% --- Import required packages ---

import matplotlib.pyplot as plt

#%% --- Helper Functions ---

#%% --- Function: scrape_goodreads ---
def add_value_labels_barh(ax, spacing=5, fontsize = 12, ha = "right"):

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        x_value = rect.get_width()
        y_value = rect.get_y() + rect.get_height() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing * -1
        

        # If value of bar is negative: Place label below bar
        if x_value < 0:
            # Invert space to place label below
            space = spacing
            # Vertically align label at top
            ha = 'left'

        # Use Y value as label and format number with one decimal place
        label = "{:}".format(x_value) #Remove .1f if you don't want one decimal place

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(space, 0),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha=ha,                      # Horizontally center label
            va="center_baseline",       # Vertically align label differently for  positive and negative values.
            rotation = 0,
            fontsize = fontsize)