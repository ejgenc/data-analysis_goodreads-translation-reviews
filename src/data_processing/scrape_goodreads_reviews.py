# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
This script ingests a collection of http's to Goodreads reviews of certain books
Produces a csv file (reviews_raw) which has the following information:
    - date_scraped
    - book_id
    - review_id
    - reviewer_id
    - reviewer_name
    - review_date
    - review_rating
    - review
    
This script targets the following file:
    ../../data/external/book_data_external.xlsx
    
The resulting csv file is located at:
    ../../data/raw/goodreads_reviews_raw.csv

"""
#%% --- Import required packages ---

import os
import shutil
from pathlib import Path # To wrap around filepaths

import pandas as pd
from src.helper_functions.data_preparation_helper_functions import scrape_goodreads_reviews
#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Import data ---

#Book ID and Book HTTP data
import_fp = Path("../../data/external/book_data_external.xlsx", engine = "openpyxl")
book_id_and_http_df = pd.read_excel(import_fp)

#Goodreads login data
# --- ATTENTION! ---
#
# To the potential replicator: you MUST provide your own login credentials
# if you wish to replicate the project in your own computing environment.
#
# --- ATTENTION! ---
import_fp = Path("../../env.txt")
with open(import_fp, "r") as credentials_file:
    credentials = credentials_file.read().split("\n")

#%% --- Check for existing goodreads_reviews_raw.csv
folder_path = Path("../../data/raw")
for filename in os.listdir(folder_path):
    if filename == "goodreads_reviews_raw.csv":
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    
#%% --- specify the Selenium driver path ---

driver_path = Path("firefox_driver/geckodriver.exe")
    
#%% --- Select the data that is requested by the scraping function ---

book_id_list = list(book_id_and_http_df["book_id"])
http_list = list(book_id_and_http_df["http"])
login_id = credentials[0]
login_password = credentials[1]

#%% --- Call the scraping function ---

reviews = scrape_goodreads_reviews(book_id_list,
                                   http_list,
                                   driver_path,
                                   login_id,
                                   login_password)

#%% --- Export Data ---

export_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
reviews.to_csv(export_fp, encoding = "utf-8", index = False)
