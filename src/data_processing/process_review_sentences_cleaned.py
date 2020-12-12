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
import spacy

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/review_sentences_cleaned.csv")
review_sentences = pd.read_csv(import_fp)

#%% --- Process: create a temporary column to hold the spaCY dependency parsing output ---

nlp = spacy.load("en_core_web_sm")
review_sentences["TEMP_dependency_doc"] = review_sentences["review_sentence"].apply(nlp)

#%% --- Process: parse the spaCy doc data structure and make the necessary info explicit ---

# Create a function that makes spaCy doc dependency structure explicit 

def placeholder_func(doc):
    token_dependencies = ((token.text, token.dep_, token.head.text) for token in doc)
    token_list = []
    for item in token_dependencies:
        token_list.append(item)
    return token_list

# Create a new column that holds the explicit dependency info

review_sentences["TEMP_explicit_dependency"] = review_sentences["TEMP_dependency_doc"].apply(placeholder_func)

#%% --- Process: Drop the columns "review_sentences" and "TEMP_dependency_doc ---

unnecessary_columns = ["review_sentence", "TEMP_dependency_doc"]

review_sentences.drop(labels = unnecessary_columns,
                      axis = 1,
                      inplace = True)

#%% --- Process: expand DOWNWARDS ---

review_sentences = review_sentences.explode("TEMP_explicit_dependency").reset_index(drop = True)

#%% --- Process: expand SIDEWAYS ---

temp_subset = review_sentences["TEMP_explicit_dependency"].to_list()

temp_df = pd.DataFrame(temp_subset,
                       columns = ["token","dependency_relation","parent_token"])

review_sentences = pd.concat([review_sentences, temp_df],
                             axis = 1)

#%% --- Process : drop the column "TEMP_explicit_dependency" ---

review_sentences.drop("TEMP_explicit_dependency",
                      axis = 1,
                      inplace = True)

#%% --- Process: give each token a unique token id ---

review_sentences["token_id"] = np.arange(len(review_sentences)) + 1 
review_sentences["token_id"] = "t" + review_sentences["token_id"].astype(str)

#%% --- Process: re-order columns ---

review_sentences = review_sentences[["book_id","review_id","sentence_id",
                                    "token_id","token","dependency_relation",
                                    "parent_token", "mentions_trans"]]

#%% TEST GROUND

trans_mask = review_sentences["mentions_trans"] == True

subset = review_sentences.loc[trans_mask,:]

#%%

trans_par_mask = review_sentences["parent_token"] == "translation"

subset2 = subset.loc[trans_par_mask,:]

#%% 

final_mask = review_sentences["dependency_relation"] == "amod"

subset3 = subset2.loc[final_mask,:]

#%% --- Export data ---

# export_fp = Path("../../data/raw/tagged_sentences_raw.csv")
# review_sentences.to_csv(export_fp, encoding = "utf-8", index = False)


