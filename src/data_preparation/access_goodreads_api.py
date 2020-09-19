# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 16:12:37 2020
@author: ejgen

------ What is this file? ------
                
Lorem dolor ipsum sit amet

"""

#%% --- Import required packages ---

import json
import os
import requests # To request for an HTML file
from pathlib import Path # To wrap around filepaths
import pandas as pd
import time

#%% --- Set proper directory to assure integration with doit ---

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#%% --- Init environment variables ---

api_key = "kjJioZzdiwd9zuHNfhOzbA"
api_secret = "pLRCn8rDorTmKccu5qsjhgxMq2LtDC1bDb2fNvF0iA"

#%% --- List all book id's ---

book_ids = ["2517"]

# res = requests.get("https://www.goodreads.com/book/show.FORMAT",
#                    params={"format" : "json",
#                            "key": str(api_key),
#                            "id" : book_ids[0]
#                            })

res = requests.get("https://www.goodreads.com/book/isbn/ISBN?format=FORMAT", params={
    "format" : "json",
    "key": api_key,
    "isbn": "0375706852"})
#%%
