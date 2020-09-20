# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
Lorem dolor ipsum sit amet

"""

#%% --- Import required packages ---

import os
from bs4 import BeautifulSoup
from selenium import webdriver # For webscraping
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path # To wrap around filepaths
import pandas as pd
import time

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Prepare URL's to be searched ---

initial_http = "https://www.goodreads.com/"
search_https = ["https://www.goodreads.com/book/show/2517",
                "https://www.goodreads.com/book/show/11691",
                "https://www.goodreads.com/book/show/6282753",
                "https://www.goodreads.com/book/show/11690",
                "https://www.goodreads.com/book/show/11692",
                "https://www.goodreads.com/book/show/11693",
                "https://www.goodreads.com/book/show/28718879",
                "https://www.goodreads.com/book/show/24997390",
               "https://www.goodreads.com/book/show/11694",
               "https://www.goodreads.com/book/show/270872"]
               
                
#%% --- Create a list to hold all reviews ---

all_reviews = []

#%% --- Initialize the Firefox gecko web driver ---

driver = webdriver.Firefox(executable_path="firefox_driver/geckodriver.exe")
    
#%% --- Next Page Test ---

## password id

login_id = "ejgscrape@protonmail.com"
login_password = "ejgscrapegoodreads"

driver.get(initial_http)
time.sleep(5)
login_id_field = driver.find_element_by_id("userSignInFormEmail").send_keys(login_id)
login_password_field = driver.find_element_by_id("user_password").send_keys(login_password)
login_button = driver.find_element_by_class_name("gr-button").click()

for search_http in search_https:
    driver.get(search_http)
    time.sleep(5)
        
    i = 0
    while i <= 10:
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser").find(id="bookReviews")
        for review in soup.find_all(class_="review"):
            try:  # Get user / reviewer id
                user_id = review.find(class_="user").get("href")[11:].split("-")[0]
                #Get user name
                user_name = review.find(class_ = "user").get_text()
                # Get full review text even the hidden parts, and remove spaces and newlines
                comment = review.find(class_="readable").find_all("span")[-1].get_text(". ", strip=True)
                date = review.find(class_="reviewDate").get_text()
                user_data = [user_id, user_name, comment, date]
                all_reviews.append(user_data)
                
            except Exception:
                print("OOOPS!")
          
        next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
        try:
            driver.execute_script("arguments[0].click();", next_button)
        except:
            next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
            driver.execute_script("arguments[0].click();", next_button)
        
        time.sleep(3)
        i += 1


driver.close()
#%% --- Write the data into a pandas DataFrame object. ---

reviews_df = pd.DataFrame.from_records(all_reviews,
                                       columns = ["user_id", "user_name",
                                                  "comment", "comment_date"])

#%% --- Save the data ---

output_fp = Path("../../data/raw/goodreads_reviews_raw.csv")
reviews_df.to_csv(output_fp, encoding = "utf-8", index = False)

            
            