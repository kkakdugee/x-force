#----------------------------------------------------
# helper.py imports
#----------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import requests
import feedparser
import time
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

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

MASTER_STOP_WORDS = list(ENGLISH_STOP_WORDS).append("inf")

#----------------------------------------------------
# General DB Functions
#----------------------------------------------------
def reset_papers_db() -> None:
    """
    Resets/overwrites the "complete_db.csv" database. USE WITH CAUTION.

    Returns
        None

    Example
        reset_papers_db()
    """
    # Warning menu
    while True:
        user_input = input("Are you sure you want to run this function? This wipes the ENTIRE existing complete_db.csv database! (y/n)")
        if user_input == "y":
            print("Proceeding to wipe the entire database.")
            break
        elif user_input == "n":
            print("Function canceled.")
            return None
        else:
            print("Wrong input. Please type 'y' or 'n'.")

    # Saving data to csv
    df = pd.DataFrame(columns=MASTER_CSV_COLUMNS)
    try:
        df.to_csv("../data/complete_db.csv", index=False)
        print("Saved!")
    except:
        print("Failed to save...")

    # Return
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
        print(f"Removed {post_len - pre_len} duplicates ({pre_len} -> {post_len})!")

    database.to_csv("../data/complete_db.csv", index=False)
    print("De-duplicated version saved!")
    
    return None

def map_yes_no(input: str) -> int:
    """ 
    Maps y/n -> 1/0. All other values are returned as is.

    input -> str
        Given "y" or "n".
    
    Returns -> int
        1 if "y", 0 elif "n", the original value otherwise.
    
    Example
        map_yes_no("y")
    """
    if input == "y":
        return 1
    elif input == "n":
        return 0
    else:
        return input

#----------------------------------------------------
# Module Checking
#----------------------------------------------------
def main():
    return None

if __name__ == "__main__":
    main()
