# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
Lorem dolor ipsum sit amet

"""

#%% --- Import required packages ---

import regex as re
import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import nltk

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
reviews_df = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- make it all lowercase ---

reviews_df["comment_lowercase"] = reviews_df["comment"].str.lower()

#%% --- Tokenize ---

reviews_df["comment_tokenized"] = reviews_df["comment_lowercase"].apply(nltk.word_tokenize)

#%% --- Create regex pattern for translation / translator ---

pat = r"\btransl\w+\b"

reviews_df["is_about_trans"] = reviews_df["comment"].str.contains(pat,
                                                                  regex = True)

print(reviews_df["is_about_trans"].sum())

#%% -- Translation subset ---

reviews_trans_mask = reviews_df["is_about_trans"] == True
reviews_trans = reviews_df.loc[reviews_trans_mask, ["comment"]] 

#%% -- Tokenize as sentences --

sents = pd.DataFrame(reviews_trans["comment"].apply(nltk.sent_tokenize).explode(ignore_index = True))

#%% --- Subset sents as containing trans ---

#Tag
sents["is_about_trans"] = sents["comment"].str.contains(pat,
                                                        regex = True)
print(sents["is_about_trans"].sum())

#Subset

sents_trans_mask = sents["is_about_trans"] == True
sents_trans = sents.loc[sents_trans_mask,:]

#%% --- Tokenize and tag words ---

sents_trans.loc[:,"tokenized"] = sents_trans.loc[:,"comment"].apply(nltk.word_tokenize)

sents_trans.loc[:,"tagged"] = sents_trans.loc[:,"tokenized"].apply(nltk.pos_tag)


#%% --- Sents-sentiment ---

sents_sentiment = sents_trans.loc[:,["comment"]]

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()


sents_sentiment.loc[:,"polarity_score"] = sents_sentiment.loc[:,"comment"].apply(sid.polarity_scores)

#%% --- Sents-pos
sents_pos = sents_trans.loc[:,["comment", "tagged"]]

adjectives = []
for index, row in sents_pos.iterrows():
    tagged = row["tagged"]
    adjectives = []
    for tag_pair in tagged:
        word = tag_pair[0]
        tag = tag_pair[1]
        # adjectives = []
        if tag in ["JJ", "JJR", "JJS"]:
            adjectives.append(word)
        
        
    