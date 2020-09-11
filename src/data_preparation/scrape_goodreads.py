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
import requests # To request for an HTML file
from selenium import webdriver # For webscraping
from pathlib import Path # To wrap around filepaths
import pandas as pd
from urllib.request import urlopen
import time

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Prepare URL's to be searched ---

initial_http = "https://www.goodreads.com/"
search_http = "https://www.goodreads.com/book/show/2517"
#search_url = urlopen(search_http)
search_url = requests.get(search_http, headers={
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        })

#%% --- Initialize the Chrome web driver ---

#Access the options for Chrome webdrivers
option = webdriver.ChromeOptions()

#Add some exceptions to deactivate images and javascript
#This way, the page will load faster.
prefs = {'profile.default_content_setting_values': {'images':2}}
option.add_experimental_option('prefs', prefs)

#Initiate the Google Chrome webdriver with options.
#driver = webdriver.Chrome("selenium chrome driver/chromedriver.exe", options=option)

#%% --- Next Page Test ---

## password id

login_id = "ejgscrape@protonmail.com"
login_password = "ejgscrapegoodreads"


#Initiate the Google Chrome webdriver with options.
driver = webdriver.Chrome("selenium chrome driver/chromedriver.exe", options=option)
driver.get(initial_http)
time.sleep(5)
login_id_field = driver.find_element_by_id("userSignInFormEmail").send_keys(login_id)
login_password_field = driver.find_element_by_id("user_password").send_keys(login_password)
login_button = driver.find_element_by_class_name("gr-button").click()

driver.get(search_http)
time.sleep(5)

from selenium.webdriver.common.action_chains import ActionChains

reviews = []

i = 0
while i < 5:
    
    
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
            reviews.append(user_data)
            
        except Exception:
            print("OOOPs!")
    
    
    
    ActionChains(driver).move_to_element(driver.find_element_by_class_name('next_page')).perform()
    next_button = driver.find_element_by_class_name('next_page')
    next_button.click()
    time.sleep(10)
    i += 1



#%% --- Do the actual scraping ---

# reviews = []
# soup = BeautifulSoup(search_url.content, "html.parser").find(id="bookReviews")
# for review in soup.find_all(class_="review"):
#         try:  # Get user / reviewer id
#             user_id = review.find(class_="user").get("href")[11:].split("-")[0]
#             #Get user name
#             user_name = review.find(class_ = "user").get_text()
#             # Get full review text even the hidden parts, and remove spaces and newlines
#             comment = review.find(class_="readable").find_all("span")[-1].get_text(". ", strip=True)
#             date = review.find(class_="reviewDate").get_text()
#             user_data = [user_id, user_name, comment, date]
#             reviews.append(user_data)
            
#         except Exception:
#             print("OOOPs!")
            
            