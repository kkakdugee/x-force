#----------------------------------e------------------
# General DB Functions
#----------------------------------------------------
import pandas as pd
import numpy as np
import requests
import feedparser
import time
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
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
    # Parsing
    print("Please input the search query or queries (separated by commas).")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    user_queries = input("Search queries?")
    if user_queries == "":
        raise ValueError(f"{user_queries} empty string is invalid. Please input a real query.")
    queries = [i.strip() for i in user_queries.split(",")]
    print("\n", end="")
    
    # Parsing
    print("Please input the additional search parameters (separated by commas). Hit ENTER for default values.")
    print("Format. starting index, number of papers, report data changes (y,n), remove duplicates (y,n)")
    print("Default. '0, 25, y, y'")
    print("This will save the papers starting at the 0th paper and ending on the 24th paper (total 25 papers saved), will show changes to the database, and will exclude saving duplicates.")
    user_params = input("Query parameters?")
    if user_params == "":
        print("Default options indicated!")
        start, max_results, verbose, remove_dupes = 0, 25, 1, 1
    else:
        start, max_results, verbose, remove_dupes = [int(helper.map_yes_no(i.strip())) for i in user_params.split(",")]
    print("\n", end="")

    # Function
    arxiv.pull_requests(queries=queries, start=start, max_results=max_results, verbose=verbose, remove_dupes=remove_dupes)
    print("Completed!")
    print("\n", end="")
    return None

def option_graph_pub_freq(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the .graph_freq() method on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.graph_pub_freq() with given inputs

    Example
        option_graph_pub_freq(current_session)
    """
    # Parsing
    print("Please input your search query or queries (separated by commas). Hit ENTER for default.")
    print("Default. 'ALL'")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    user_queries = input("Search queries?")
    if user_queries == "":
        print("Default option indicated.")
        queries = ["ALL"]
    else:
        queries = [i.strip() for i in user_queries.split(",")]
    print("\n", end="")

    # Parsing
    print("Please input source restriction or restrictions (separated by commas). Hit ENTER for default.")
    print("Default. 'ALL'")
    print("Eg. 'arxiv, scopus'")
    user_params = input("Query parameters?")
    if user_params == "":
        print("Default option indicated.")
        sources = ["ALL"]
    else:
        sources = [i.strip() for i in user_params.split(",")]
    print("\n", end="")

    # Function Call
    current_session.graph_pub_freq(queries=queries, sources=sources)

    # Return
    print("Completed!")
    print("\n", end="")
    return None

def option_report_db_summary(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; runs the db_sumarry methods on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.report_db_summary()
        Runs current_session.graph_db_summary()

    Example
        option_graph_pub_freq(current_session)
    """
    # Function Call
    current_session.report_db_summary()
    current_session.graph_db_summary()
    
    # Return
    print("Completed!")
    print("\n", end="")
    return None

def option_graph_text_freq(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the .graph_text_count() method on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.graph_text_freq() with given inputs

    Example
        option_graph_text_freq(current_session)
    """
    # Parsing
    print("Please input your search query or queries (separated by commas). Hit ENTER for default.")
    print("Default. 'ALL'")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    user_queries = input("Search queries?")
    if user_queries == "":
        print("Default option indicated.")
        queries = ["ALL"]
    else:
        queries = [i.strip() for i in user_queries.split(",")]
    print("\n", end="")

    print("Please input source restriction or restrictions (separated by commas). Hit ENTER for default.")
    print("Default. 'ALL'")
    print("Eg. 'arxiv, scopus'")
    user_params = input("Query parameters?")
    if user_params == "":
        print("Default option indicated.")
        sources = ["ALL"]
    else:
        sources = [i.strip() for i in user_params.split(",")]
    print("\n", end="")

    print("Please additional search paramaters (separated by commas). Hit ENTER for default.")
    print("Format: 'text_mode, type_mode'")
    print("Default. 'word, abstract'")
    print("text_mode can be (char/word), type_mode can be (title/abstract)")
    user_add_params = input("Query parameters?")
    if user_add_params == "":
        print("Default option indicated.")
        text_mode, type_mode = "word", "abstract"
    else:
        text_mode, type_mode = [i.strip() for i in user_add_params.split(",")]
    print("\n", end="")

    # Function Call
    current_session.graph_text_freq(queries=queries, sources=sources, text_mode=text_mode, type_mode=type_mode)
    print("NOTE: If the graph is empty, that means that the queried term does not exist within the given source!")
    print("Eg. If you searched for 'radiation' within the 'scopus' dataset, if no papers with that term exist in the local scopus database, then an empty graph will appear.")

    # Return
    print("Completed!")
    print("\n", end="")
    return None

def option_graph_keyword_freq(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the .graph_keyword_freq() method on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.graph_keyword_freq() with given inputs

    Example
        option_graph_keyword_freq(current_session)
    """
    # Parsing
    print("Please input your search query or queries (separated by commas). Hit ENTER for default.")
    print("Default. 'ALL'")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    user_queries = input("Search queries?")
    if user_queries == "":
        print("Default option indicated.")
        queries = ["ALL"]
    else:
        queries = [i.strip() for i in user_queries.split(",")]
    print("\n", end="")

    print("Please input source restriction or restrictions (separated by commas). Hit ENTER for default.")
    print("Default. 'ALL'")
    print("Eg. 'arxiv, scopus'")
    user_params = input("Query parameters?")
    if user_params == "":
        print("Default option indicated.")
        sources = ["ALL"]
    else:
        sources = [i.strip() for i in user_params.split(",")]
    print("\n", end="")

    print("Please additional search paramaters (separated by commas). Hit ENTER for default.")
    print("Format: 'type_mode, k, n_gram'")
    print("Default. 'abstract, 15, 1'")
    print("type_mode can be (title/abstract), k is the top k results returned, n_grams is number of words in token")
    user_add_params = input("Query parameters?")
    if user_add_params == "":
        print("Default option indicated.")
        type_mode, k, n_gram = "abstract", 15, 1
    else:
        type_mode, k, n_gram = [i.strip() for i in user_add_params.split(",")]
    print("\n", end="")

    # Function Call
    current_session.graph_keyword_freq(queries=queries, sources=sources, type_mode=type_mode, k=int(k), n_gram=int(n_gram))
    
    # Return
    print("Completed!")
    print("\n", end="")
    return None

def option_graph_text_count(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the .graph_text_count() method on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.graph_text_count() with given inputs

    Example
        option_graph_pub_freq(current_session)
    """
    print("Please input the search query or queries (separated by commas) or 'ALL' if you want to graph all.")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    print("Eg. 'ALL'")
    user_queries = input("Search queries?")
    queries = [i.strip() for i in user_queries.split(",")]

    print("Please input paramater restrictions (separated by commas). Otherwise, if you want the default values, hit ENTER key again.")
    print("Format: 'source, text_mode, type_mode'")
    print("Eg. 'arxiv', 'word', 'title'")
    print("Eg. ''")
    print("The first example will analyze the word count of titles of papers from arxiv. The second example (which is the empty string) means default values.")
    user_params = input("Query parameters?")

    if user_params == "":
        current_session.graph_text_count(queries=queries)
    else:
        source, text_mode, type_mode = [i.strip() for i in user_queries.split(",")]
        current_session.graph_text_count(queries=queries, source=source, text_mode=text_mode, type_mode=type_mode)
    
    print("Completed!", end="\n\n")
    return None

def option_graph_keyword_freq(current_session: eda_graphing.XForce_Grapher) -> None:
    """ 
    Helper function for menu-navigation; parses user inputs and then feeds into the .graph_keyword_freq() method on current_session class.

    current_session -> arxiv.XForce_Grapher
        The given arxiv.XForce_Grapher object for which to graph the frequencies
    
    Returns -> None
        Runs current_session.graph_keyword_freq() with given inputs

    Example
        option_graph_keyword_freq(current_session)
    """
    print("Please input the search query or queries (separated by commas) or 'ALL' if you want to graph all.")
    print("Eg. 'radiation, plasmonics, metamaterials'")
    print("Eg. 'ALL'")
    user_queries = input("Search queries?")
    queries = [i.strip() for i in user_queries.split(",")]

    print("Please input paramater restrictions (separated by commas). Otherwise, if you want the default values, hit ENTER key again.")
    print("Format: 'source, type_mode', 'k', 'n_gram'")
    print("Eg. 'arxiv', 'title', '15', '2")
    print("Eg. ''")
    print("The first example will find the top 15 keywords (bigrams) of titles of papers from arxiv. The second example (which is the empty string) means default values.")
    user_params = input("Query parameters?")

    if user_params == "":
        current_session.graph_keyword_freq(queries=queries)
    else:
        source, type_mode, k, n_gram = [i.strip() for i in user_queries.split(",")]
        current_session.graph_keyword_freq(queries=queries, source=source, type_mode=type_mode, k=k, n_gram=n_gram)
    
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
        ["[Update] Add more papers to database", option_arxiv_update],
        ["[Analyze] See database paper distribution", option_report_db_summary],
        ["[Analyze] See publication frequency by query", option_graph_pub_freq],
        ["[Analyze] See keyword frequency by query", option_graph_keyword_freq],
        ["[Analyze] See text frequency by query", option_graph_text_freq],
        ["[Update] Remove paper dupes from database", option_clean_dupes]
    ]
    hard_options = {
        "e": ["[Menu] Exit program", option_exit],
        "w": ["[Update] Wipe entire paper database", option_wipe],
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
    print("Welcome to Team NLP Research and Data Viz's Data Project!")
    print("\n", end="")
    menu = menu_creator()
    while True:
        while True:
            current_session = eda_graphing.XForce_Grapher()
            menu_print(menu)
            print_options = [key for key in menu.keys()]
            user_input = input(f"Pick your option: {print_options}. ")
            print("\n", end="")
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