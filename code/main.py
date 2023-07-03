#----------------------------------------------------
# General DB Functions
#----------------------------------------------------

import pandas as pd
import numpy as np
import requests
import feedparser
import time
from datetime import datetime
import sys
sys.path.append("./code/Modules/")
import helper
import arxiv
import eda_graphing

#----------------------------------------------------
# Main
#----------------------------------------------------
def main() -> None:

    print("Welcome!")
    current_session = eda_graphing.XForce_Grapher()

    while True:
        while True:
            print("========")
            print("Menu")
            print("========")
            print("1. Update database by search term from arxiv")
            print("2. Visualizations by search term")
            print("3. Summary of database")
            print("4. Clean dupes from database")
            print("e. Exit program")
            print("w. Wipe database")
            user_input = input("Pick your option (1-4, e, w).")
            if user_input not in {"w","1","2","3","4","e"}:
                print("Invalid answer. Please input an integer from this list (1-4) or letter from this list (e, w).", end="\n")
            else:
                break

        if user_input == "1":
            print("--")
            print("Please input the search query or queries (separated by commas).")
            print("Eg. 'radiation, plasmonics, metamaterials'")
            user_queries = input("Search queries?")
            
            print("--")
            print("Please input the additional search parameters (separated by commas).")
            print("The format is [starting index, number of papers, report data changes (y,n), remove duplicates (y,n)]")
            print("Eg. '5, 10, n, y'")
            print("This will save the papers starting at the 5th paper and ending on the 14th paper (for total of 10 papers saved), won't show the data changes to the database, and will exclude saving duplicates.")
            user_params = input("Query parameters?")

            queries = [i.strip() for i in user_queries.split(",")]
            start, max_results, verbose, remove_dupes = [i.strip() for i in user_params.split(",")]
            arxiv.pull_requests(queries=queries, start=start, max_results=max_results, verbose=verbose, remove_dupes=remove_dupes)

            print("Completed!")
        elif user_input == "2":
            print("--")
            print("Please input the search query or queries (separated by commas).")
            print("Eg. 'radiation, plasmonics, metamaterials'")
            user_queries = input("Search queries?")

            print("--")
            print("Please input source restriction, if any. Currently, only one source can be queried at a time. If there are no restrictions, hit ENTER key again.")
            print("Eg. 'arxiv'")
            print("Eg. ''")
            print("The first example will only analyze papers pulled from arxiv. The second example (which is the empty string) means you have no restrictions and the analysis will be performed on the entire database.")
            user_params = input("Query parameters?")
            if user_params == "":
                user_params = "ALL"

            queries = [i.strip() for i in user_queries.split(",")]
            for query in queries:
                current_session.graph_freq(query, user_params)
            print("Completed!")
        elif user_input == "3":
            helper.db_summary()
            print("Completed!")
        elif user_input == "4":
            helper.remove_dupes()
            print("Completed!")
        elif user_input == "e":
            is_exiting = True
            break
        elif user_input == "w":
            helper.reset_papers_db()
            print("Completed!")
    print("Thank you for using this program!")
    return None

if __name__ == "__main__":
    main()
