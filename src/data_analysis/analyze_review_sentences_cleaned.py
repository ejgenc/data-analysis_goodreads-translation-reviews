# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:45:43 2020

------ What is this file? ------
                
This script ingests the file review_sentences_cleaned.csv in order to process
it into a second level of analysis

This script targets the following file:
    ../../data/cleaned/review_sentences_cleaned.csv
    
The resulting csv file is located at:
    ../../data/analysis_results/review_sentences_analyzed.csv
    
"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/review_sentences_cleaned.csv")
review_sentences = pd.read_csv(import_fp)

#%% --- Analyze: calculate sentence length (in words), count stopwords too ---

review_sentences["length_in_words"] = review_sentences["review_sentence"].str.split(" ").str.len()

#%% --- Analyze: tag sentence if it mentions "AUTHOR / BOOK" 

# ATTENTION! The tagging process below is at alpha. It will be much more
# complex in the finished version.

#%% --- Analyze: tag sentence if it mentions TRANSLATION / TRANSLATOR ###

# ATTENTION! The tagging process below is at alpha. It will be much more
# complex in the finished version.

pattern = r"\b[Tt]ransl\w+\b"

review_sentences["mentions_trans"] = review_sentences["review_sentence"].str.contains(pattern)

#%% --- Analyze: calculate sentiment for each sentence using VADER

#Create an instance of the sentiment analyzer
sid = SentimentIntensityAnalyzer()

#Create a temporary list_of_dics to hold sentiment score matrixes
temp_VADER_list_of_dicts = (review_sentences["review_sentence"].apply(sid.polarity_scores)).to_list()

#Create a dataframe from the list of dicts
temp_VADER_df = pd.DataFrame(temp_VADER_list_of_dicts)

#Change the column names of the temporary VADER dataframe
temp_VADER_df.columns = ["VADER_score_neg","VADER_score_neu",
                         "VADER_score_pos","VADER_score_compound"]

#Concat temp_VADER_df and review_sentences
review_sentences = pd.concat([review_sentences,temp_VADER_df],
                             axis = 1)
#%% --- Export Data ---

export_fp = Path("../../data/analysis_results/review_sentences_analyzed.csv")
review_sentences.to_csv(export_fp, encoding = "utf-8", index = False)