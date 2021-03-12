# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 22:45:18 2021

@author: ejgen

------ What is this file? ------

This script ingests the file modifiers_raw.csv in order to format it
according to some pre-determined quality standarts.

This script targets the following file:
    ../../data/raw/modifiers_raw.csv
    
The resulting csv file is located at:
    ../../data/cleaned/modifiers_cleaned.csv
    
Reports related to the cleaning process are located at:
    ../../data/cleaning_reports/...
    
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

import_fp = Path("../../data/raw/modifiers_raw.csv")
modifiers = pd.read_csv(import_fp, encoding = "utf-8")

#%% --- Cleaning: filter, document and drop null values ---

#Create a mask for null values
null_values_mask = modifiers.isnull()

# null_values_mask.sum().sum() != 0, so there are null values

#%% --- Cleaning: assure data type agreement between and within columns ---

error_list = []

for column_name in modifiers.columns:
    expected_dtype = type(modifiers[column_name][0])
    value_index = 0
    while value_index < len(modifiers[column_name]):
        actual_dtype = type(modifiers[column_name][value_index])
        if expected_dtype != actual_dtype:
            error_entry = [column_name, value_index, expected_dtype, actual_dtype]
            error_list.append(error_entry)
        value_index += 1
        
# There appears to be no proof of data-type disagreement. Moving on.

#%% --- Cleaning: drop specific modifiers that are known false positives ---

#There are some specific modifiers whose exclusion from the final data
#can be justified. See below for a list:
#   - Adjectives that denote language (English translation, French translator etc.)

#Create a non-comprehensive list of languages
languages_list = ["chinese","spanish","english","hindi","bengali",
                  "portuguese","russian","japanese","turkish","korean",
                  "french","german","vietnamese","urdu","italian","arabic",
                  "persian","polish","romanian","dutch","greek","hungarian",
                  "czech","finnish","irish","norwegian","swedish","danish",
                  "lithuanian","latvian","estonian","georgian","armenian",
                  "azerbaijani"]

#Create a mask based on these languages
language_modifiers_mask = modifiers["modifier"].isin(languages_list)
reverse_language_modifiers_mask = ~language_modifiers_mask

#Use the above boolean masks to filter
unacceptable_modifier_forms = modifiers[language_modifiers_mask]
modifiers = modifiers[reverse_language_modifiers_mask]

#%% --- Cleaning: clean modified variation ---

# !!! IMPORTANT NOTE: Why this method and not more strict reg-ex matching? !!!
# The method that I've used to parse the dependency structure of each sentence
# Is RegEx based. For each word that I wanted to capture, I  wrote some
# broad RegEx that tries to match in a way that mimics lemma matching.
# Howecer, it becomes apparent here that this method has resulted in some 
# false positives that need correction here.
# This question arises: why not use strict matching in the first place?
# Well, I have two arguments against this: - RegEx matching requires
# less code in the first place
# - This is an iterative process. How can I know what to include without
# seeing the results first? To me, casting the net wide and
#then trimming down seems to be a better strategy when faced with uncertainty.

# Use string methods to clean some faulty string endings
modifiers["modified"] = modifiers["modified"].str.strip("-!.,[]()")

# Filter out the rest, allowing only known variations 

#Take a look at existing variations
modified_variations = modifiers["modified"].unique()

#Compile a list of acceptable ones
acceptable_modified_forms = ["translation", "translations",
                              "translation's", "translations'",
                              "translator", "translators",
                              "translator's", "translators'",
                              "style", "styles","style's", "styles'",
                              "book", "books", "book's", "books'",
                              "author", "authors", "author's", "authors'",
                              "writer", "writers", "writer's", "writers'",
                              "writing", "writings", "writing's", "writings'",
                              "translate", "translates", "translated",
                              "translating", "write", "writes", "wrote",
                              "written"]

#Create a boolean mask based on what is acceptable and what is not
acceptable_modified_forms_mask = modifiers["modified"].isin(acceptable_modified_forms)
reverse_acceptable_modified_forms_mask = ~acceptable_modified_forms_mask

#Use the above boolean masks to filter
unacceptable_modified_forms = modifiers[reverse_acceptable_modified_forms_mask]
modifiers = modifiers[acceptable_modified_forms_mask]

#Take a look at existing variations again
modified_variations = modifiers["modified"].unique()

#%% --- Export data ---

export_fp = Path("../../data/cleaned/modifiers_cleaned.csv")
modifiers.to_csv(export_fp, encoding = "utf-8", index = False)

#%% --- Export cleaning documentation ---

cleaning_documentation_dataframes = [unacceptable_modifier_forms,
                                      unacceptable_modified_forms]
cleaning_documentation_filenames = ["modifiers_raw_unacceptable_modifiers.csv",
                                    "modifiers_rawunacceptable_modifieds.csv"]

for dataframe, filename in zip(cleaning_documentation_dataframes,
                               cleaning_documentation_filenames):
    export_fp = Path("../../data/cleaning_reports/{}".format(filename))
    dataframe.to_csv(export_fp, encoding = "utf-8", index = False)


