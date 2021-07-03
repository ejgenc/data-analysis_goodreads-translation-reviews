# -*- coding: utf-8 -*-
"""
Created on Tue Apr  6 14:49:35 2021

@author: ejgen

------ What is this file? ------

This script targets the files goodreads_reviews_analyzed.csv and related files,
gathering book level statistics about things like number of reviews on the
Goodreads website/number of reviews scraped, total/mean review length etc.

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

#%% --- Analyze: number of and percentage reviews per book. ---
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

#percentage lost after cleaning
book_statistics["perc_lost_after_cleaning"] = (1
                                               - (book_statistics["n_final_reviews"]
                                               / book_statistics["n_initial_reviews"]))

#%% --- Analyze: total and mean review length in sentences / words ---

# total review length in words and sets
total_review_lengths = (review_statistics
                        .groupby("book_id")
                         [["total_length_in_words",
                          "total_length_in_sentences"]]
                         .agg(["sum"])
                         .reset_index()
                         .droplevel(0, axis = 1))

total_review_lengths.columns = ["book_id",
                                "total_rev_length_in_words",
                                "total_rev_length_in_sents"]

# mean review length in words and sentences 

mean_lengths_in_words = (review_statistics
                         .groupby("book_id")
                         ["total_length_in_words"]
                         .agg(["sum","count"])
                         .reset_index())
mean_lengths_in_words["mean_rev_length_in_words"] = (mean_lengths_in_words["sum"]
                                                        / mean_lengths_in_words["count"])

mean_lengths_in_sents = (review_statistics
                         .groupby("book_id")
                         ["total_length_in_sentences"]
                         .agg(["sum","count"])
                         .reset_index())
mean_lengths_in_sents["mean_rev_length_in_sents"] = (mean_lengths_in_sents["sum"]
                                                            / mean_lengths_in_sents["count"])

lengths = [total_review_lengths, mean_lengths_in_words, mean_lengths_in_sents]

for i, mean_lengths in enumerate(lengths):
    if "sum" in mean_lengths.columns:
        mean_lengths = (mean_lengths
                        .drop(["sum", "count"],
                              axis = 1))
        lengths[i] = mean_lengths
        
    book_statistics = (book_statistics
                       .merge(mean_lengths,
                              how = "left",
                              on = "book_id"))


#%% --- Analyze: share of different mentions ---

share_types = ["share_of_only_trans_mentions", "share_of_trans_mentions",
               "share_of_only_orig_mentions", "share_of_orig_mentions"]

for share_type in share_types:
    share = (review_statistics.loc[:, ["book_id",
                                       "total_length_in_sentences",
                                       share_type]]
             .groupby("book_id")
             .agg("sum")
             .assign(temp = lambda x: (x[share_type]
                                       / x["total_length_in_sentences"]))
             .drop(["total_length_in_sentences", share_type],
                   axis = 1)
             .rename({"temp": share_type},
                     axis = 1)
             .reset_index())
    
    book_statistics = (book_statistics
                       .merge(share,
                              how = "left",
                              on = "book_id"))
    
#%% --- Export data ---

export_fp = Path("../../data/analysis_results/book_level_statistics.csv")
book_statistics.to_csv(export_fp, encoding = "utf-8", index = False)
