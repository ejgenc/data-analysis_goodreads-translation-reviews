# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:04:35 2020

@author: ejgen


------ What is this file? ------
                
This script ingests the file tokens_and_dependencies_cleaned.csv
in order to process it into a second level of analysis

This script targets the following file:
    ../../data/cleaned/tokens_and_dependencies_cleaned.csv
    
The resulting csv files are located at:
    ../../data/raw/trans_tokens_and_dependencies_raw.csv
    ../../data/raw/orig_tokens_and_dependencies_raw.csv
    
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

import_fp = Path("../../data/cleaned/tokens_and_dependencies_cleaned.csv")
tokens_and_dependencies = pd.read_csv(import_fp)

#%% --- Process: seperate dataset into tokens whose sentences ---
#   --- Explicitly state translation vs. original ---

# Translation

trans_mask = tokens_and_dependencies["sent_mentions_trans"] == True
trans_tokens_and_dependencies = tokens_and_dependencies.loc[trans_mask,:]

# Original


#%% --- Translation processing ---

#Create a regex pattern for translation

trans_pat = r"\b[Tt]ransl\w+\b"
non_trans_pat = r"\bis\b|\bare\b"

#PATTERN 1
# dependency_relation = "amod"
# parent_token = trans_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "amod"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_1_extract = trans_tokens_and_dependencies.loc[merged_mask,:]

# PATTERN 2
#dependency_relation = "acomp"
#parent_token = non_trans_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "acomp"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(non_trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_2_extract = trans_tokens_and_dependencies.loc[merged_mask,:]

# PATTERN 3
#dependency_relation = "advmod"
#parent_token = trans_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "advmod"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_3_extract = trans_tokens_and_dependencies.loc[merged_mask,:]

# PATTERN 4 - Step one
#token = trans_pat
#dependency_relation = nsubj
#parent_token = non_trans_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "nsubj"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(non_trans_pat)
token_mask = trans_tokens_and_dependencies["token"].str.match(trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & token_mask

#Use mask to extract
pat_4_sent_ids = trans_tokens_and_dependencies.loc[merged_mask,"sentence_id"]

#PATTERN 4 - Step two
#dependency_relation = "acomp"
#parent_token = non_trans_pat
#sentence_id = pat_4_sent_ids

#Create appropriate masks
sentence_id_mask = trans_tokens_and_dependencies["sentence_id"].isin(pat_4_sent_ids.values)
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "acomp"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(non_trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & sentence_id_mask

pat_4_extract = trans_tokens_and_dependencies.loc[merged_mask,:]


#%%

import spacy
nlp = spacy.load("en_core_web_sm")

#%%
sents = ["bad translation",
         "bad translations",
         "a bad translation",
         "the bad translation",
         "the bad translations",
         "translations are bad",
         "the translation is bad",
         "the translations are bad",
         "the newest translation is bad",
         "the translation of the book is bad",
         "horribly translated",
         "well translated",
         "the translator did a great job"]

dependency_docs = []

for sent in sents:
    dependency_doc = nlp(sent)
    dependency_docs.append(dependency_doc)
    
#%%

def placeholder_func(doc):
    token_dependencies = ((token.text, token.dep_, token.head.text) for token in doc)
    token_list = []
    for item in token_dependencies:
        token_list.append(item)
    return token_list

explicit_dependencies = []

for doc in dependency_docs:
    explicit_dependency = placeholder_func(doc)
    explicit_dependencies.append(explicit_dependency)
