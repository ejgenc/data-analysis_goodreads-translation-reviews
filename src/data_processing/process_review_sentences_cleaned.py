# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:45:43 2020

------ What is this file? ------
                
This script ingests the file review_sentences_cleaned.csv in order to transform
it into another dataset.

This script targets the following file:
    ../../data/cleaned/review_sentences_cleaned.csv
    
The resulting csv file is located at:
    ../../data/raw/tokens_and_dependencies_raw.csv
    
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
tokens_and_dependencies = pd.read_csv(import_fp)

#%% --- Process: create a temporary column to hold the spaCY dependency parsing output ---

nlp = spacy.load("en_core_web_sm")
tokens_and_dependencies["TEMP_dependency_doc"] = tokens_and_dependencies["review_sentence"].apply(nlp)

#%% --- Process: parse the spaCy doc data structure and make the necessary info explicit ---

# Create a function that makes spaCy doc dependency structure explicit 

def placeholder_func(doc):
    token_dependencies = ((token.text, token.dep_, token.head.text) for token in doc)
    token_list = []
    for item in token_dependencies:
        token_list.append(item)
    return token_list

# Create a new column that holds the explicit dependency info

tokens_and_dependencies["TEMP_explicit_dependency"] = tokens_and_dependencies["TEMP_dependency_doc"].apply(placeholder_func)

#%% --- Process: Drop the columns "tokens_and_dependencies" and "TEMP_dependency_doc ---

unnecessary_columns = ["review_sentence", "TEMP_dependency_doc"]

tokens_and_dependencies.drop(labels = unnecessary_columns,
                      axis = 1,
                      inplace = True)

#%% --- Process: expand DOWNWARDS ---

tokens_and_dependencies = tokens_and_dependencies.explode("TEMP_explicit_dependency").reset_index(drop = True)

#%% --- Process: expand SIDEWAYS ---

temp_subset = tokens_and_dependencies["TEMP_explicit_dependency"].to_list()

temp_df = pd.DataFrame(temp_subset,
                       columns = ["token","dependency_relation","parent_token"])

tokens_and_dependencies = pd.concat([tokens_and_dependencies, temp_df],
                             axis = 1)

#%% --- Process : drop the column "TEMP_explicit_dependency" ---

tokens_and_dependencies.drop("TEMP_explicit_dependency",
                      axis = 1,
                      inplace = True)

#%% --- Process: give each token a unique token id ---

tokens_and_dependencies["token_id"] = np.arange(len(tokens_and_dependencies)) + 1 
tokens_and_dependencies["token_id"] = "t" + tokens_and_dependencies["token_id"].astype(str)

#%% --- Process: re-order columns ---

tokens_and_dependencies = tokens_and_dependencies[["book_id","review_id","sentence_id",
                                    "token_id","sent_mentions_original",
                                    "sent_mentions_trans","token",
                                    "dependency_relation","parent_token"]]

#%% --- Export data ---

export_fp = Path("../../data/raw/tokens_and_dependencies_raw.csv")
tokens_and_dependencies.to_csv(export_fp, encoding = "utf-8", index = False)


