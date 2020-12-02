# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This script ingests the file goodreads_reviews_cleaned.csv in order to process
it into a second level or analysis

This script targets the following file:
    ../../data/cleaned/goodreads_reviews_cleaned.csv
    
The resulting csv file is located at:
    ../../data/raw/review_sentences_raw.csv
    
"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
import re #regex
import nltk
from nltk.tokenize import sent_tokenize

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/goodreads_reviews_cleaned.csv")
review_sentences = pd.read_csv(import_fp)

#%% --- Process: drop unnecessary columns ---

unnecessary_columns = ["date_scraped", "reviewer_id", "reviewer_name",
                       "review_date", "rating"]

review_sentences.drop(labels = unnecessary_columns,
                      axis = 1,
                      inplace = True)

review_sentences.reset_index(drop = True)

#%% --- Process: tokenize reviews into sentences ---

review_sentences["review"] = review_sentences["review"].apply(sent_tokenize)

#%% --- Process: expand individual sentences into different rows for tidy data ---

review_sentences = review_sentences.explode("review").reset_index(drop = True)

#%% --- Process: rename "review" column to "review_sentence"

review_sentences.rename({"review": "review_sentence"},
                        axis = "columns",
                        inplace = True)

#%% --- Process: tag each sentence with a sentence id ---

review_sentences["sentence_id"] = np.arange(len(review_sentences))
review_sentences["sentence_id"] = "s" + review_sentences["sentence_id"].astype(str)

# #%% --- Process: calculate sentence length (in words), count stopwords too ---

# review_sentences["length_in_words_with_stopwords"] = review_sentences["review_sentence"].str.split().str.len()

#%% --- Process: tag sentence if it mentions "AUTHOR / BOOK" 

# ATTENTION! The tagging process below is at alpha. It will be much more
# complex in the finished version.

# #%% --- Process: tag sentence if it mentions TRANSLATION / TRANSLATOR ###

# # ATTENTION! The tagging process below is at alpha. It will be much more
# # complex in the finished version.

# pattern = r"\b[Tt]ransl\w+\b"

# review_sentences["mentions_trans"] = review_sentences["review_sentence"].str.contains(pattern)
#%% -- Process: re-order columns ---

# re-ordering scheme: book/review/sentence id's line up, 
# tags come after id's
# extra data comes after tags
# the actual sentence comes last

review_sentences = review_sentences[["book_id", "review_id", "sentence_id","review_sentence"]]

#%% --- Export data ---

# export_fp = Path("../../data/raw/review_sentences_raw.csv")
# review_sentences .to_csv(export_fp, encoding = "utf-8", index = False)


