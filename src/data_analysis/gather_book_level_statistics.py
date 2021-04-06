# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:49:35 2021

@author: ejgen

------ What is this file? ------

This script targets the files goodreads_reviews_analyzed.csv and related files,
gathering book level statistics about things like number of reviews on the
Goodreads website/number of reviews scraped, total/mean review length etch.

This script targets the following files:
    ../../data/external/book_data_external.xlsx
    ../../data/raw/goodreads_reviews_raw.csv
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
    
The resulting csv file is located at:
    ../../data/analysis_results/book_level_statistics.csv

"""
#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---
#Also features some quick data processing

import_fp = Path("../../data/external/book_data_external.xlsx")
book_statistics = pd.read_excel(import_fp,
                          engine="openpyxl",
                          usecols = ["book_id","book_name","author"])

import_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
inital_reviews = (pd.read_csv(import_fp)
                  .loc[:,["book_id","review_id"]])

import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
final_reviews = (pd.read_csv(import_fp)
                 .loc[:,["book_id","review_id"]])

import_fp = Path("../../data/analysis_results/goodreads_reviews_analyzed.csv")
review_statistics = (pd.read_csv(import_fp)
                     .drop(["date_scraped","reviewer_id",
                            "reviewer_name","review_date",
                            "review"],
                           axis = 1))

#%% --- Analyze: number of reviews per book. ---
# Number of reviews per book is calculated in tree different conditions:
# n_reviews_in_goodreads = number of reviews present on the site
# n_inital_reviews = number of reviews scraped
# n_final_reviews = number of reviews left after cleaning

n_inital_reviews = (inital_reviews
                    .groupby("book_id")
                    ["book_id"]
                    .agg(["count"])
                    .rename({"count": "n_initial_reviews"},
                            axis = 1))

n_final_reviews = (final_reviews
                   .groupby("book_id")
                   ["book_id"]
                   .agg(["count"])
                   .rename({"count": "n_final_reviews"},
                           axis = 1))

book_statistics = (book_statistics
                    .merge(n_inital_reviews,
                          how = "left",
                          on = "book_id")
                    .merge(n_final_reviews,
                           how = "left",
                           on = "book_id"))

#percentage lost after scraping
#percentage lost after cleaning

book_statistics["perc_lost_after_cleaning"] = (1
                                               - (book_statistics["n_final_reviews"]
                                               / book_statistics["n_initial_reviews"]))





