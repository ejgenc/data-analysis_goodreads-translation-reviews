# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:04:35 2020

@author: ejgen


------ What is this file? ------
                
This script ingests and processes the file
tokens_and_dependencies_cleaned.csv to find which adverbs/adjectives
are used with the specified RegEx patterns.

This script targets the following file:
    ../../data/cleaned/tokens_and_dependencies_cleaned.csv
    
The resulting csv files are located at:
    ../../data/raw/trans_tokens_and_dependencies_raw.csv
    ../../data/raw/orig_tokens_and_dependencies_raw.csv
    
"""

import os
from pathlib import Path # To wrap around filepaths
import pandas as pd
import numpy as np

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

original_mask = tokens_and_dependencies["sent_mentions_original"] == True
original_tokens_and_dependencies = tokens_and_dependencies.loc[original_mask,:]
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

#Add an extra "refers_to" column
pat_1_extract.loc[:,"refers_to"] = pat_1_extract.loc[:,"parent_token"]

#Reset and drop index
pat_1_extract.reset_index(drop = True,inplace = True)

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
pat_2_token_ids = trans_tokens_and_dependencies.loc[merged_mask,"token_id"]

def add_number_to_token_id(token_id,num):
    num_part = int(token_id.split("t")[1])
    num_part += num
    new_id = "t" + str(num_part)
    return new_id

pat_2_token_ids_two_away = pat_2_token_ids.apply(add_number_to_token_id,args = [2])

#               --- Step Two ---

#dependency_relation = "acomp"
#parent_token = verb_pat
#sentence_id = pat_2_sent_ids
# token_id =  pat_2_token_ids_two_away

#Create appropriate masks
sentence_id_mask = trans_tokens_and_dependencies["sentence_id"].isin(pat_2_sent_ids.values)
token_id_mask = trans_tokens_and_dependencies["token_id"].isin(pat_2_token_ids_two_away.values)
dependency_relation_mask = trans_tokens_and_dependencies["dependency_relation"] == "acomp"
parent_token_mask = trans_tokens_and_dependencies["parent_token"].str.match(verb_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & sentence_id_mask & token_id_mask

pat_2_extract = trans_tokens_and_dependencies.loc[merged_mask,:]

#Reset and drop index
pat_2_extract.reset_index(drop = True,inplace = True)

#           --- Step Three ---

#Since i want pat_2_extract to specify what exactly it is referring to
# (think of "good-acomp-translator"), I have to go back two id's,
#get the nsubj and substitute it.

#Multi-step pandas shenaningans to get that data

pat_2_extract_token_ids = pat_2_extract.loc[:,"token_id"]
pat_2_extract_token_ids_two_up = pat_2_extract_token_ids.apply(add_number_to_token_id,args = [-2])
pat_2_extract_token_ids_two_up_mask =  trans_tokens_and_dependencies.loc[:,"token_id"].isin(pat_2_extract_token_ids_two_up.values)
pat_2_extract_correct_parents = trans_tokens_and_dependencies.loc[pat_2_extract_token_ids_two_up_mask,"token"]
pat_2_extract_correct_parents.reset_index(drop = True,inplace = True)

pat_2_extract.loc[:,"refers_to"] = pat_2_extract_correct_parents

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

#Add an extra "refers_to" column
pat_3_extract.loc[:,"refers_to"] = pat_3_extract.loc[:,"parent_token"]

#Reset and drop index
pat_3_extract.reset_index(drop = True,inplace = True)


#%%         --- Merge translation processing extracts ---

translation_extracts = pd.concat([pat_1_extract,
                                 pat_2_extract,
                                 pat_3_extract],
                                 axis = 0,
                                 ignore_index = True
                                )

#%%     --- Original Processing ---

#Create a regex pattern for original

book_pat = r"\b[Bb]ook[\w+]?\b"
style_pat = r"\b[Ss]tyle[\w+]?\b"
author_pat = r"\b[Aa]uthor[\w+]?\b"
write_pat = r"\b[Ww]r[io]t\w+\b"

combined_noun_pat = r"\b[Bb]ook[\w+]?\b|\b[Ss]tyle[\w+]?\b|\b[Aa]uthor[\w+]?\b|\b[Ww]r[io]t\w+\b"

verb_pat = r"\bis\b|\bare\b|\bwas\b|\bwere\b|\bbe\b"

#%%         --- PATTERN 4 ---

# dependency_relation = "amod"
# parent_token = book_pat | style_pat | author_pat | writer_pat

#Create appropriate masks
dependency_relation_mask = original_tokens_and_dependencies["dependency_relation"] == "amod"
parent_token_mask = original_tokens_and_dependencies["parent_token"].str.match(combined_noun_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_4_extract = original_tokens_and_dependencies.loc[merged_mask,:]

#Add an extra "refers_to" column
pat_4_extract.loc[:,"refers_to"] = pat_4_extract.loc[:,"parent_token"]

#Reset and drop index
pat_4_extract.reset_index(drop = True,inplace = True)

#%%         --- PATTERN 5 ---
#               --- Step One ---

#token = book_pat | style_pat | author_pat
#dependency_relation = nsubj
#parent_token = verb_pat

#Create appropriate masks
dependency_relation_mask = original_tokens_and_dependencies["dependency_relation"] == "nsubj"
parent_token_mask = original_tokens_and_dependencies["parent_token"].str.match(verb_pat)
token_mask = original_tokens_and_dependencies["token"].str.match(combined_noun_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & token_mask

#Use mask to extract
pat_5_sent_ids = original_tokens_and_dependencies.loc[merged_mask,"sentence_id"]
pat_5_token_ids = original_tokens_and_dependencies.loc[merged_mask,"token_id"]

pat_5_token_ids_two_away = pat_5_token_ids.apply(add_number_to_token_id, args = [2])


#               --- Step Two ---

#dependency_relation = "acomp"
#parent_token = verb_pat
#sentence_id = pat_5_sent_ids
#token_id = pat_5_token_ids_to_away

#Create appropriate masks
sentence_id_mask = original_tokens_and_dependencies["sentence_id"].isin(pat_5_sent_ids.values)
token_id_mask = original_tokens_and_dependencies["token_id"].isin(pat_5_token_ids_two_away.values)
dependency_relation_mask = original_tokens_and_dependencies["dependency_relation"] == "acomp"
parent_token_mask = original_tokens_and_dependencies["parent_token"].str.match(verb_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask & sentence_id_mask & token_id_mask

pat_5_extract = original_tokens_and_dependencies.loc[merged_mask,:]

#Reset and drop index
pat_5_extract.reset_index(drop = True,inplace = True)

#           --- Step Three ---

#Since i want pat_2_extract to specify what exactly it is referring to
# (think of "good-acomp-translator"), I have to go back two id's,
#get the nsubj and substitute it.

#Multi-step pandas shenaningans to get that data

pat_5_extract_token_ids = pat_5_extract.loc[:,"token_id"]
pat_5_extract_token_ids_two_up = pat_5_extract_token_ids.apply(add_number_to_token_id, args = [-2])
pat_5_extract_token_ids_two_up_mask =  original_tokens_and_dependencies.loc[:,"token_id"].isin(pat_5_extract_token_ids_two_up.values)
pat_5_extract_correct_parents = original_tokens_and_dependencies.loc[pat_5_extract_token_ids_two_up_mask,"token"]
pat_5_extract_correct_parents.reset_index(drop = True,inplace = True)

pat_5_extract.loc[:,"refers_to"] = pat_5_extract_correct_parents

#%%         --- PATTERN 6 ---

#dependency_relation = "advmod"
#parent_token = write_pat

#Create appropriate masks
dependency_relation_mask = original_tokens_and_dependencies["dependency_relation"] == "advmod"
parent_token_mask = original_tokens_and_dependencies["parent_token"].str.match(write_pat)

#Merge masks
merged_mask = dependency_relation_mask & parent_token_mask

#Use mask to extract
pat_6_extract = original_tokens_and_dependencies.loc[merged_mask,:]

#Add an extra "refers_to" column
pat_6_extract.loc[:,"refers_to"] = pat_6_extract.loc[:,"parent_token"]

#Reset and drop index
pat_6_extract.reset_index(drop = True,inplace = True)

#%%         --- Merge original processing extracts ---

original_extracts = pd.concat([pat_4_extract,
                                  pat_5_extract,
                                  pat_6_extract],
                                  axis = 0,
                                  ignore_index = True
                                )

#%% --- Merge extracts together ---

extracts = pd.concat([translation_extracts,original_extracts],
                     axis = 0,
                     ignore_index = True)

#%% --- Process: add an unique modifier ID to all ---

extracts["modifier_id"] = np.arange(len(extracts)) + 1 
extracts["modifier_id"] = "m" + extracts["modifier_id"].astype(str)

#%% --- Process: drop unnecessary columns ---

extracts.drop(["sent_mentions_original",
               "sent_mentions_trans",
               "parent_token"],
              axis = 1,
              inplace = True)

#%% --- Process: rename specific columns ---

extracts.rename(columns = {"token" : "modifier",
                           "refers_to" : "modified"},
                inplace = True)


#%% --- Process: reorder columns ---


extracts = extracts[["book_id", "review_id", "sentence_id",
                     "token_id", "modifier_id", "modifier",
                     "modified","dependency_relation"]]

#%% --- Export data ---

export_fp = Path("../../data/raw/modifiers_raw.csv")
extracts.to_csv(export_fp, encoding = "utf-8", index = False)


