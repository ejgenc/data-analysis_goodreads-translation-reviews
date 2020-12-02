# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 23:45:43 2020

@author: ejgen
"""

# #%% --- Analyze: calculate sentence length (in words), count stopwords too ---

# review_sentences["length_in_words_with_stopwords"] = review_sentences["review_sentence"].str.split().str.len()

#%% --- Analyze: tag sentence if it mentions "AUTHOR / BOOK" 

# ATTENTION! The tagging process below is at alpha. It will be much more
# complex in the finished version.

# #%% --- Analyze: tag sentence if it mentions TRANSLATION / TRANSLATOR ###

# # ATTENTION! The tagging process below is at alpha. It will be much more
# # complex in the finished version.

# pattern = r"\b[Tt]ransl\w+\b"

# review_sentences["mentions_trans"] = review_sentences["review_sentence"].str.contains(pattern)

#%% --- Analyze: calculate sentiment for each sentence using VADER