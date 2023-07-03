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
def menu_creator() -> set:
    """ 
    Helper function that auto generates the user menu. Changes to the user menu should be in this function.

    Returns -> set
        User-menu printed out, along with a set of options for user control.

    Example
        menu_creator()
    """
    # Variables
    auto_options = [
        "Update database by search term from arxiv",
        "Visualizations by search term",
        "Summary of database",
        "Clean dupes from database"
    ]
    hard_options = [
        "Exit program", "e'"
        "Wipe database", "w"
    ]
    return_set = {}

    # Generation
    print("========")
    print("Menu")
    print("========")
    for index, option in enumerate(auto_options):
        print(f"{index}. {option}")
        return_set.add(str(index))
    for option in hard_options:
        print(f"{option[1]}. {option[0]}")
        return_set.add(str(option[1]))
    return return_set

def option_pull_request():
    print("Please input the search query or queries (separated by commas).")
    print("Eg. 'radiation, plasmonics, metamaterials'", end="\n")
    user_queries = input("Search queries?")
    
    print("--")
    print("Please input the additional search parameters (separated by commas).")
    print("The format is [starting index, number of papers, report data changes (y,n), remove duplicates (y,n)]")
    print("Eg. '5, 10, n, y'")
    print("This will save the papers starting at the 5th paper and ending on the 14th paper (for total of 10 papers saved), won't show the data changes to the database, and will exclude saving duplicates.", end="\n")
    user_params = input("Query parameters?")

    queries = [i.strip() for i in user_queries.split(",")]
    start, max_results, verbose, remove_dupes = [i.strip() for i in user_params.split(",")]
    arxiv.pull_requests(queries=queries, start=start, max_results=max_results, verbose=verbose, remove_dupes=remove_dupes)

    print("Completed!")

def main() -> None:

    print("Welcome!")
    current_session = eda_graphing.XForce_Grapher()
    options_pool = ""
    while True:
        while True:
            options_pool = menu_creator()
            user_input = input(f"Pick your option {options_pool}.")
            if user_input not in options_pool:
                print(f"Invalid answer. Please an input within {options_pool}", end="\n")
            else:
                break

        if user_input == "1":
            option_pull_request()
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
