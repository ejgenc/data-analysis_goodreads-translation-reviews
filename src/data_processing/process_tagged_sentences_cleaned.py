# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 16:38:13 2020

@author: ejgen

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
import pandas as pd
from ast import literal_eval

#!!! ATTENTION !!!#
#Pandas does not preserve list structure when saving data to a .csv file.
#Because of this, we need to re-create the column "tagged_sentence" using
# literal_eval.
# More information about literal_eval can be found here:
# https://docs.python.org/3/library/ast.html

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

import_fp = Path("../../data/cleaned/tagged_sentences_cleaned.csv")
tagged_sentences = pd.read_csv(import_fp)
tagged_sentences["tagged_sentence"] = tagged_sentences["tagged_sentence"].apply(literal_eval)

#%% --- Process: select only the tagged sentences where mentions_trans == True ---

# Create a boolean mask for mention_trans == True
trans_mask = tagged_sentences["mentions_trans"] == True

#Subset the data according to that mask
tagged_sentences = tagged_sentences.loc[trans_mask,:].reset_index(drop = True)

#%% --- Process: tag sentences where "translation" is "nn"

def tag_for_translation_nn(list_of_tuples):
    return ("translation","nn") in list_of_tuples

tagged_sentences["translation_as_noun"] = tagged_sentences["tagged_sentence"].apply(tag_for_translation_nn)

#%% --- Export data ---

# export_fp = Path("../../data/raw/relevant_words_raw.csv")
# tagged_sentences.to_csv(export_fp, encoding = "utf-8", index = False)

#%%

a = tagged_sentences["tagged_sentence"]

print(("translation", "NN") in a[501])
