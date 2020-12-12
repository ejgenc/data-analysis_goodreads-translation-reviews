# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:45:43 2020

------ What is this file? ------
                
This script ingests the file review_sentences_cleaned.csv in order to transform
it into another dataset.

This script targets the following file:
    ../../data/cleaned/review_sentences_cleaned.csv
    
The resulting csv file is located at:
    ../../data/raw/syntax_trees_raw.csv
    
"""
#%% --- Import required packages ---

import os
from pathlib import Path # To wrap around filepaths
import numpy as np
import pandas as pd
from nltk import pos_tag, word_tokenize

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/review_sentences_cleaned.csv")
review_sentences = pd.read_csv(import_fp)

#%% --- Process: create a new column "tagged_sentence" that tokenizes and tags review_sentence

#Use NLTK tagger to tag POS
review_sentences["tagged_sentence"] = review_sentences["review_sentence"].apply(word_tokenize)

review_sentences["tagged_sentence"] = review_sentences["tagged_sentence"].apply(pos_tag)

#%% --- Process: drop "review_sentence" column ---

review_sentences.drop("review_sentence",
                      axis = 1,
                      inplace = True)

#%% --- Process: give an unique id to each tagged_sentence ---

review_sentences["tagged_sentence_id"] = np.arange(len(review_sentences))
review_sentences["tagged_sentence_id"] = "ts" + review_sentences["tagged_sentence_id"].astype(str)

#%% --- Process: re-order columns ---

review_sentences = review_sentences[["book_id","review_id",
                                     "sentence_id", "tagged_sentence_id",
                                     "mentions_trans", "tagged_sentence"]]

#%% --- Export data ---

export_fp = Path("../../data/raw/tagged_sentences_raw.csv")
review_sentences.to_csv(export_fp, encoding = "utf-8", index = False)


