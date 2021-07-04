# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

"""
#%% --- Import required packages ---

from bs4 import BeautifulSoup
from selenium import webdriver # For webscraping
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import date

# --- Helper Functions ---

#%% --- Function: scrape_goodreads ---

def scrape_goodreads_reviews(book_id_list,
                             http_list,
                             selenium_gecko_driver_path,
                             login_id,
                             login_password):
    
    # Set the starting page for goodreads
    initial_http = "https://www.goodreads.com/"
    
    # Initialize the web driver
    driver = webdriver.Firefox(executable_path = selenium_gecko_driver_path)
    
    # Go to the page, wait five seconds for the page to load
    driver.get(initial_http)
    time.sleep(5)
    
    # Handle login using credentials
    # SUBFUNCTION - HANDLE GOODREADS LOGIN
    login_id_field = driver.find_element_by_id("userSignInFormEmail").send_keys(login_id)
    login_password_field = driver.find_element_by_id("user_password").send_keys(login_password)
    login_button = driver.find_element_by_class_name("gr-button").click()
    
    # Create an empty list that will hold all review info
    reviews_data = []
    
    #Create a global review_id_enumerator that will track
    #how many reviews there are in total
    review_id_enumerator = 1
    
    # Go through the https #
    for index, http in enumerate(http_list, start = 0):
        # Keeping track of which book_id we are in
        book_id = book_id_list[index]
        
        driver.get(http)
        time.sleep(5)
        
        #Initialize a counter for page count in review pages
        # Since the maximum number of pages allowed by Goodreads is 10,
        # we'll be looping only up to ten
        i = 0
        while i <= 10:
            
            #Here, we are using BeautifulSoup to locate where to go
            #on the page
            page_source = driver.page_source #The source of the current page
            #Within the page, find the section title "bookreviews"
            soup = BeautifulSoup(page_source, "html.parser").find(id="bookReviews")
            for review in soup.find_all(class_="review"):
                date_scraped = date.today().strftime("%d/%m/%Y")
                review_id = "r{}".format(review_id_enumerator)
                try:
                    reviewer_id = review.find(class_="user").get("href")[11:].split("-")[0]
                    reviewer_name = review.find(class_ = "user").get_text()
                    review_date = review.find(class_="reviewDate").get_text()
                    rating = len(review.find_all(class_="p10"))
                    review = review.find(class_="readable").find_all("span")[-1].get_text(". ", strip=True)
                    
                    user_data = [date_scraped, book_id, review_id, reviewer_id,
                                 reviewer_name, review_date, rating,
                                 review]
                    
                    reviews_data.append(user_data)
                    
                except Exception:
                    print("Something has gone wrong during the parsing of individual reviews.")
                    
                review_id_enumerator += 1
            
            next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
            try:
                driver.execute_script("arguments[0].click();", next_button)
            except:
                next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, 'next_page')))
                driver.execute_script("arguments[0].click();", next_button)
                
            time.sleep(3)
            i += 1
        
    driver.close()
    reviews_df = pd.DataFrame.from_records(reviews_data,
                                           columns = ["date_scraped","book_id", "review_id",
                                                      "reviewer_id", "reviewer_name",
                                                      "review_date","rating",
                                                      "review"])
    return reviews_df
