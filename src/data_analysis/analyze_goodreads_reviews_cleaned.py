# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:35:39 2021

@author: ejgen

------ What is this file? ------

This script targets the files goodreads_reviews_cleaned.csv and
review_sentences_analyzed.csv, calculating summary statistics such as
review length and sentiment score.

This script targets the following files:
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    ../../data/analysis_results/review_sentences_analyzed.csv
    
The resulting csv file is located at:
    ../../data/analysis_results/goodreads_reviews_analyzed.csv
        
"""

#%% --- Import required packages ---

import os

from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

#goodreads_reviews_cleaned
import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
goodreads_reviews = pd.read_csv(import_fp, encoding = "utf-8")

#review_sentences_analyzed
import_fp = Path("../../data/analysis_results/review_sentences_analyzed.csv")
sentences_analyzed = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Prepare data ---

sentences_analyzed = sentences_analyzed.loc[:,["review_id",
                                               "sentence_id",
                                               "sent_mentions_original",
                                               "sent_mentions_trans",
                                               "length_in_words",
                                               "VADER_score_compound"]]

# Take a subset of goodreads reviews to include only reviews whose review no
# appear in sentences_analyzed.

rid_mask = goodreads_reviews["review_id"].isin(sentences_analyzed["review_id"])
goodreads_reviews = goodreads_reviews.loc[rid_mask, :]
#%% --- Analyze: review length in sentences and words. ---

length_per_review = (sentences_analyzed
                        .groupby("review_id")
                        ["length_in_words"]
                        .agg(["sum","count"])
                        .rename({"sum" : "total_length_in_words",
                                 "count" : "total_length_in_sentences"},
                                axis = 1)
                        .reset_index())

goodreads_reviews = goodreads_reviews.merge(length_per_review,
                                            how = "left",
                                            on = "review_id")

#%% --- Analyze: review length in sentences and words, split by mentions.---

orig_mention_mask = sentences_analyzed["sent_mentions_original"] == True
trans_mention_mask = sentences_analyzed["sent_mentions_trans"] == True
only_orig_mention_mask = (orig_mention_mask & ~trans_mention_mask)
only_trans_mention_mask = (~orig_mention_mask & trans_mention_mask)
both_mention_mask = (orig_mention_mask & trans_mention_mask)
both_nomention_mask = (~orig_mention_mask & ~trans_mention_mask)

masks = [only_orig_mention_mask, only_trans_mention_mask,
         both_mention_mask, both_nomention_mask]

prefixes = [("length_in_sents_of_orig_mentions", "length_in_words_of_orig_mentions"),
            ("length_in_sents_of_trans_mentions", "length_in_words_of_trans_mentions"),
             ("length_in_sents_of_both_mentions", "length_in_words_of_both_mentions"),
             ("length_in_sents_of_none_mentions", "length_in_words_of_none_mentions")]

for mask, prefix in zip(masks,prefixes):
    masked_length_per_review = (sentences_analyzed[mask].
                                groupby("review_id")
                                ["length_in_words"]
                                .agg(["sum","count"])
                                .rename({"sum" : prefix[0],
                                         "count" : prefix[1]},
                                        axis = 1)
                                .reset_index())
    
    goodreads_reviews = (goodreads_reviews.merge(masked_length_per_review,
                                                how = "left",
                                                on = "review_id")
                                          .fillna(value = 0,
                                                  axis = 0))

#%% --- Analyze: VADER score for the whole review ---

VADER_score_per_review = (sentences_analyzed
                          .groupby("review_id")
                          ["VADER_score_compound"]
                          .agg(["sum","count"])
                          .reset_index())

VADER_score_per_review["avg_VADER_score"] = (VADER_score_per_review["sum"]
                                             / VADER_score_per_review["count"])

VADER_score_per_review = VADER_score_per_review.drop(labels = ["sum","count"],
                                                     axis = "columns")

goodreads_reviews = goodreads_reviews.merge(VADER_score_per_review,
                                            how = "left",
                                            on = "review_id")

