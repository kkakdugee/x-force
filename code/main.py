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
sys.path.append("../code/Modules/")
import helper
import arxiv
import eda_graphing

#----------------------------------------------------
# Main Helper
#----------------------------------------------------
def option_exit(dummy_var) -> None:
    """ 
    Helper function for menu-navigation; calls simulates a break via an raise error syntax.

    This asks for a dummy_var argument because option_visualize() requires an actual variable.
    Due to limitations of Python's try-except block, adding a dummy variable to this function ensures a workaround for an "all-cases" user input.
    """
    raise StopIteration

def option_wipe(dummy_var) -> None:
    """ 
    Helper function for menu-navigation; calls helper.reset_papers_db().

    This asks for a dummy_var argument because option_visualize() requires an actual variable.
    Due to limitations of Python's try-except block, adding a dummy variable to this function ensures a workaround for an "all-cases" user input.

    Returns -> None
        Runs helper.reset_papers_db().

    Example
        option_wipe(dummy_var)
    """
    helper.reset_papers_db()
    print("Completed!", end="\n\n")
    return None

def option_arxiv_update(dummy_var) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the pull_requests() function.

    This asks for a dummy_var argument because option_visualize() requires an actual variable.
    Due to limitations of Python's try-except block, adding a dummy variable to this function ensures a workaround for an "all-cases" user input.

    Returns -> None
        Runs pull_requests()

    Example
        option_arxiv_update(dummy_var)
    """
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
    start, max_results, verbose, remove_dupes = [int(helper.map_yes_no(i.strip())) for i in user_params.split(",")]
    arxiv.pull_requests(queries=queries, start=start, max_results=max_results, verbose=verbose, remove_dupes=remove_dupes)

    print("Completed!", end="\n\n")
    return None

def option_visualize(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the .graph_freq() method on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.graph_freq()

    Example
        option_visualize(current_session)
    """
    print("Please input the search query or queries (separated by commas).")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    user_queries = input("Search queries?")

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
    print("Completed!", end="\n\n")
    return None

def option_db_summary(dummy_var) -> None:
    """ 
    Helper function for menu-navigation; calls helper.db_summary().

    This asks for a dummy_var argument because option_visualize() requires an actual variable.
    Due to limitations of Python's try-except block, adding a dummy variable to this function ensures a workaround for an "all-cases" user input.

    Returns -> None
        Runs helper.db_summary().

    Example
        option_db_summary(dummy_var)
    """
    helper.db_summary()
    print("Completed!", end="\n\n")
    return None

def option_clean_dupes(dummy_var) -> None:
    """ 
    Helper function for menu-navigation; calls helper.remove_dupes().

    This asks for a dummy_var argument because option_visualize() requires an actual variable.
    Due to limitations of Python's try-except block, adding a dummy variable to this function ensures a workaround for an "all-cases" user input.

    Returns -> None
        Runs helper.remove_dupes().

    Example
        option_clean_dupes(dummy_var)
    """
    helper.remove_dupes()
    print("Completed!", end="\n\n")
    return None

def menu_creator() -> dict:
    """ 
    Auto generate the user menu, which takes on the form of a dictionary. Changes to the user menu should be made in this function.

    Returns -> dict
        User menu options and functions stored as a dictionary object.

    Example
        menu = menu_creator()
    """
    # Variables
    auto_options = [
        ["Update database by search term from arxiv", option_arxiv_update],
        ["Visualizations by search term", option_visualize],
        ["Summary of database", option_db_summary],
        ["Clean dupes from database", option_clean_dupes]
    ]
    hard_options = {
        "e": ["Exit program", option_exit],
        "w": ["Wipe database", option_wipe],
    }
    menu = {}
    for i, v in enumerate(auto_options):
        menu[str(i)] = v
    for k, v in hard_options.items():
        menu[k] = v

    return menu

def menu_print(menu: dict) -> None:
    """ 
    Prints out a given dictionary, typically used with the results of menu_creator().

    Returns -> None
        Prints out the given dictionary.

    Example
        menu_print(menu)
    """
    print("========")
    print("Menu")
    print("========")
    for k, v in menu.items():
        print(f"{k}. {v[0]}")
    return None

#----------------------------------------------------
# Main
#----------------------------------------------------
def main() -> None:
    print("Welcome!")
    current_session = eda_graphing.XForce_Grapher()
    menu = menu_creator()
    while True:
        while True:
            menu_print(menu)
            print_options = [key for key in menu.keys()]
            user_input = input(f"Pick your option: {print_options}.")
            if user_input not in menu.keys():
                print(f"Invalid answer. Please an input within {print_options}", end="\n\n")
            else:
                break

        try:
            menu[user_input][1](current_session)
        except StopIteration:
            break
            
    print("Thank you for using this program!")
    return None

if __name__ == "__main__":
    main()
