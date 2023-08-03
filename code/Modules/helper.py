#----------------------------------------------------
# helper.py imports
#----------------------------------------------------
# API
import requests # HTTP requests
from bs4 import BeautifulSoup
import feedparser
import time
from datetime import datetime
from dotenv import load_dotenv # Loading environment variables (API KEY)
from typing import List, Dict 
import csv # Creating and Manipulating CSV files
import os # For accessing the env file
import random

# EDA/NLP
import pandas as pd
import numpy as np
from numpy import ma
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.colors import Normalize
import re
import string
from sklearn.feature_extraction.text import CountVectorizer
import nltk
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import networkx as nx
from scipy import sparse
from wordcloud import WordCloud
from textblob import TextBlob
from keybert import KeyBERT
import circlify

# APP
import streamlit as st

# Menu
import sys

# Misc
import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

#----------------------------------------------------
# arXiv API Defaults
#----------------------------------------------------
DEFAULT_BASE_URL = "https://export.arxiv.org/api/"
DEFAULT_METHOD = "query"
DEFAULT_URL = DEFAULT_BASE_URL + DEFAULT_METHOD
DEFAULT_SEARCH_QUERY = "radiation"
DEFAULT_DATE_QUERY = "2010-01-01" # year-mo-day
ARXIV_VIEW_LIMIT = 30000
ARXIV_FETCH_LIMIT = 2000
MAX_STEP_SIZE = ARXIV_FETCH_LIMIT
MAX_VIEW_SIZE = ARXIV_VIEW_LIMIT
MIN_WAIT_TIME = 3 # seconds
DEFAULT_PARAMS = {"search_query": DEFAULT_SEARCH_QUERY,
                  "sortBy": 'submittedDate',
                  "sortOrder": 'descending',
                  "start": 0,
                  "max_results": 25
                  }

#----------------------------------------------------
# arXiv Data Extract Defaults
#----------------------------------------------------
ARXIV_KEYS = ["title", 
              "arxiv_journal_ref", 
              "authors", 
              "arxiv_doi", 
              "published", 
              "summary", 
              "link", 
              "tags"
              ]

MASTER_CSV_COLUMNS = ["source",
                      "query",
                      "query_time",
                      "title",
                      "journal",
                      "authors",
                      "doi",
                      "published",
                      "abstract",
                      "url",
                      "tags"
                      ]

META_CSV_COLUMNS = ["query",
                    "target_date_paper_url",
                    "target_date_paper_title",
                    "target_date_paper_publish_date",
                    "start_index",
                    "target_date",
                    "date_of_last_index_extraction"
                    ]

TEMP_STOP_WORDS = stopwords.words('english')
TEMP_STOP_WORDS.append("inf")
MASTER_STOP_WORDS = TEMP_STOP_WORDS

#----------------------------------------------------
# General Filepaths Variables
#----------------------------------------------------
# from perspective of app.py
DEFAULT_DATABASE_FILEPATH = "../../data/complete_db.csv" 
DEFAULT_CURR_WORKING_DATABASE_FILEPATH = "../../data/curr_filtered_db.csv"

COMPLETE_DATABASE_FILEPATH = "../../data/complete_db.csv"
DEFAULT_FOLDER_FOR_DATABASE_FILEPATH = "../../data/"

RELATIVE_TO_MODULES_COMPLETE_DB = "../data/complete_db.csv"
RELATIVE_TO_MODULES_DATA = "../data/"

#----------------------------------------------------
# General DB Functions
#----------------------------------------------------
def reset_papers_db() -> None:
    print("This function has been moved to db_functions.py instead of helper.py. Renamed as reset_db.")
    return None

def remove_dupes(verbose: int=1) -> None:
    print("This function has been moved to db_functions.py instead of helper.py.")
    return None

def remove_dupes(verbose: int=1) -> None:
    """ 
    Manually remove duplicates in complete_db.csv of duplicate arvix entries.

    verbose -> int
        0: suppresses reporting on changes to the database
        1: reports on changes to database
    
    Returns -> None
        complete_db.csv is clean of duplicates via the "url" column
    
    Example
        remove_dupes()
    """
    database = pd.read_csv("../data/complete_db.csv")
    
    if verbose == 1:
        pre_len = len(database)
    
    database = database[~database.duplicated("url")]
    
    if verbose == 1:
        post_len = len(database)
        print(f"Removed {pre_len - post_len} duplicates ({pre_len} -> {post_len})!")

    database.to_csv("../data/complete_db.csv", index=False)
    print("De-duplicated version saved!")
    
    return None

def map_yes_no(input: str, index: int) -> int:
    """ 
    Maps y/n -> 1/0. All other valid values are returned as is.

    input -> str
        Given "y" or "n".
    
    input -> index
        Given the index of the passed input
    
    Returns -> int
        1 if "y", 0 elif "n", the original value if valid, and None otherwise.
    
    Example
        map_yes_no("y")
    """
    if input.isdigit() and (index == 0):
        return input
    elif input == "y" and (index == 1):
        return 1
    elif input == "n" and (index == 1):
        return 0
    else:
        return None
    
def generate_boolean_conditions(mode: str, conditions: list) -> str:
    """ 
    Given list of conditions, generate the boolean syntax for a dataframe.

    mode -> str
        The given mode
        query: Boolean expression is created with indexing into query column
        source: Boolean expression is created with indexing into source column

    conditions -> list
        The given list of conditions
    
    Returns -> str
        Returns the condition expressions
    
    Example
        generate_boolean_conditions("query", ["radiation", "plasmonics"])
    """
    # Input Error Handling
    mode_options = {"query", "source"}
    if mode not in mode_options:
        raise ValueError(f"{mode} invalid, must be {mode_options}")
    
    # Function
    condition_prefix = f"df['{mode}'] == "
    expression = " | ".join([f"({condition_prefix}'{condition}')" for condition in conditions])
    
    # Return
    return expression

#----------------------------------------------------
# Module Checking
#----------------------------------------------------
def main():
    return None

if __name__ == "__main__":
    main()
