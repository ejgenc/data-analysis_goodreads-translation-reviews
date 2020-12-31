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

#!!!! TEST REGEX MATCHING !!!!
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

#%% --- Process: single out tokens of importance ---
#   --- Explicitly state translation vs. original ---

# Translation

trans_mask = tokens_and_dependencies["sent_mentions_trans"] == True
trans_tokens_and_dependencies = tokens_and_dependencies.loc[trans_mask,:]

# Original



#%%     --- Translation processing ---

#Create a regex pattern for translation

trans_pat = r"\b[Tt]ranslat\w+\b"
verb_pat = r"\bis\b|\bare\b|\bwas\b|\bwere\b|\bbe\b"

#%%         --- PATTERN 1 ---

# dependency_relation = "amod"
# parent_token = trans_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "amod"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_1_extract = trans_tokens_and_dependencies.loc[merged_mask,:]

#%%         --- PATTERN 2 ---
#               --- Step One ---

#token = trans_pat
#dependency_relation = nsubj
#parent_token = verb_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "nsubj"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(verb_pat)
token_mask = trans_tokens_and_dependencies["token"].str.match(trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & token_mask

#Use mask to extract
pat_2_sent_ids = trans_tokens_and_dependencies.loc[merged_mask,"sentence_id"]

#               --- Step Two ---

#dependency_relation = "acomp"
#parent_token = verb_pat
#sentence_id = pat_2_sent_ids

#Create appropriate masks
sentence_id_mask = trans_tokens_and_dependencies["sentence_id"].isin(pat_2_sent_ids.values)
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "acomp"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(verb_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & sentence_id_mask

pat_2_extract = trans_tokens_and_dependencies.loc[merged_mask,:]


#%%         --- PATTERN 3 ---

#dependency_relation = "advmod"
#parent_token = trans_pat

#Create appropriate masks
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "advmod"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(trans_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_3_extract = trans_tokens_and_dependencies.loc[merged_mask,:]


#%%         --- Merge translation processing extracts ---

translation_extracts = pd.concat([pat_1_extract,
                                 pat_2_extract,
                                 pat_3_extract],
                                 axis = 0,
                                 ignore_index = True
                                )

#%%     --- Original Processing ---

#Create a regex pattern for translation

book_pat = r"\b[Bb]ook[\w+]\b"
style_pat = r"\b[Ss]tyle[\w+]\b"
author_pat = r"\b[Aa]uthor[\w+]\b"
write_pat = r"\b[Ww]r[io]t\w+\b"
verb_pat = r"\bis\b|\bare\b|\bwas\b|\bwere\b|\bbe\b"

#%%         --- PATTERN 4 ---

# dependency_relation = "amod"
# parent_token = book_pat | style_pat

#%%         --- PATTERN 5 ---

#               --- Step One ---

#token = book_pat | style_pat
#dependency_relation = nsubj
#parent_token = verb_pat

#               --- Step Two ---

#dependency_relation = "acomp"
#parent_token = verb_pat
#sentence_id = pat_5_sent_ids


#%%         --- PATTERN 6 ---

#dependency_relation = "advmod"
#parent_token = book_pat | style_pat

#%%         --- Merge original processing extracts ---

# original_extracts = pd.concat([pat_4_extract,
#                                  pat_5_extract,
#                                  pat_6_extract],
#                                  axis = 0,
#                                  ignore_index = True
#                                 )

#%% --- Process: drop unnecessary columns ---


# #%% --- Export data ---

# filenames_and_extacts = {"translation_modifiers" : translation_extracts,
#                          "original_modifiers" : original_extracts}

# for filename, extract in filenames_and_extracts.items:
#     export_fp = Path("../../data/raw/{}_raw.csv").format(filename)
#     extract.to_csv(export_fp, encoding = "utf-8", index = False)


#%% --- TEST GROUND ----


import spacy
nlp = spacy.load("en_core_web_sm")

#%%
sents = ["a bad translation",
         "a bad and horrible translation",
         "the translation is bad",
         "the translation was bad",
         "the translation will be bad",
         "the translation were bad",
         "the translation is bad and horrible",
         "the translations are bad",
         "the translations are bad and horrible",
         "badly translated",
         "translated badly",
         "translated by maureen freely"]

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
