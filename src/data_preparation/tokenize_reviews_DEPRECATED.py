# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
Lorem dolor ipsum sit amet

"""

#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import nltk
nltk.download('vader_lexicon')

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
reviews_df = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Tokenize each review to sentences ---

reviews_df["reviews_tokenized_as_sentences"] = reviews_df["comment"].apply(nltk.sent_tokenize)

# --- Get the sentiment score for each review ---



#%% --- Tokenize each sentence to words ---

#reviews_df["reviews_tokenized_as_words"] = reviews_df["reviews_tokenized_as_sentences"].apply(nltk.word_tokenize) 

#%%

example_text = reviews_df.loc[0,"comment"]

example_tokenized_sent = nltk.sent_tokenize(example_text)
example_tokenized_word = nltk.word_tokenize(example_text)
example_tokenized_word_2 = [nltk.word_tokenize(x) for x in example_tokenized_sent]


example_word = example_tokenized_word_2[0]
a = nltk.pos_tag(example_word)

#%%
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
for sentence in example_tokenized_sent:
    print(sentence)
    ss = sid.polarity_scores(sentence)
    for k in sorted(ss):
         print('{0}: {1}, '.format(k, ss[k]), end='')
    print()
    
total_score = 0
for sentence in example_tokenized_sent:
    ss = sid.polarity_scores(sentence)
    total_score += ss["compound"]
    
