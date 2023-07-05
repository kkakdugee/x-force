#----------------------------------------------------
# Imports Checking
#----------------------------------------------------
import pandas as pd
import numpy as np
import requests
import feedparser
import time
from datetime import datetime
import sys
import helper

#----------------------------------------------------
# Query Functions
#----------------------------------------------------
def fetch_request(query: str=helper.DEFAULT_SEARCH_QUERY, start: int=0, max_results: int=25) -> feedparser.util.FeedParserDict:
    """
    Performs a fetch request using the arXiv API, returning the most recently published results first.

    query -> str
        The given search query for arxiv to find papers on

    start -> int
        The index of the papers at which to start pulling data on

    max_results -> int
        The total number of papers after `start` to pull from; cannot exceed the value stored in helper.ARXIV_FETCH_LIMIT

    Returns -> feedparser.util.FeedParserDict
        A feedparser.util.FeedParserDict object that contains the JSON parsed data
    
    Example
        feed = fetch_request(query=search_term, 10, 50)
        Query "radiation" returns 30,000 (default API behavior). For our slice, return the 11th article on the list (10th index) up to 49th article on the list, returning 50 total articles.
    """
    if max_results > helper.ARXIV_FETCH_LIMIT:
        raise ValueError(f"Your query size is too large and will result in an IP ban. The limit is {helper.ARXIV_FETCH_LIMIT}.")
    else:
        # Request setup
        params = {
            "search_query": query,
            "sortBy": 'submittedDate',
            "sortOrder": 'descending',
            "start": start,
            "max_results": max_results
        }
        response = requests.get(helper.DEFAULT_URL, params=params)

        # Sleep to prevent rate limit
        print(f"Sleeping {helper.MIN_WAIT_TIME}")
        time.sleep(helper.MIN_WAIT_TIME)

        # Return
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            print(f"Fetched {len(feed.entries)} entries.")
            return feed
        else:
            raise ConnectionError(response.status_code)

def parse_request(feed: feedparser.util.FeedParserDict, query: str, verbose: int=1) -> pd.core.frame.DataFrame:
    """
    Converts the given JSON feed file into a legible dataframe (useful for .csv storage).

    feed -> feedparser.util.FeedParserDict
        The given JSON object from feedparser

    query -> str
        The query term that was used to generate the feed. This is not enforced to be correct, so users need to manually double-check that this field is correct.
        Used in .csv saving.

    verbose -> int
        0: suppresses all missing-data-points reporting
        1: at the end of script, summarize the total number of missing data points
        
    Returns -> pd.core.frame.DataFrame
        The JSON object converted to a dataframe

    Example
        search_term = "radiation"
        feed = fetch_request(query=search_term, 10, 50)
        df = parse_request(feed, query=search_term)
    """
    # Parsing
    all_papers = []
    num_missing_keys = 0
    for paper in feed.entries:
        paper_data = ["arxiv", query, datetime.now()]
        for key in helper.ARXIV_KEYS:
            try:
                if key == "summary":
                    paper_data.append(paper[key].replace("\n", " "))
                elif key == "authors":
                    paper_data.append([item["name"] for item in paper[key]])
                elif key == "link":
                    paper_data.append(paper[key][:-2])
                else:
                    paper_data.append(paper[key])
            except:
                paper_data.append(np.nan)
                num_missing_keys += 1
        all_papers.append(paper_data)
    if verbose == 1:
        print(f"{num_missing_keys} missing keys.")
    df = pd.DataFrame(data=all_papers, columns=helper.MASTER_CSV_COLUMNS)
    print("Parsed!")
    return df

def helper_fetch_parse_request(query: str=helper.DEFAULT_SEARCH_QUERY, start: int=0, max_results: int=25, verbose: int=1) -> pd.core.frame.DataFrame:
    """
    Helper function for the main fetch_parse_request() function.

    query -> str
        The given search query for arxiv to find papers on

    start -> int
        The index of the papers at which to start pulling data on

    max_results -> int
        The total number of papers after `start` to pull from; cannot exceed the value stored in helper.ARXIV_FETCH_LIMIT

    verbose -> int
        0: suppresses all missing-data-points reporting
        1: at the end of script, summarize the total number of missing data points
        
    Returns -> pd.core.frame.DataFrame
        The fetch results converted as dataframe.
    """
    feed = fetch_request(query=query, start=start, max_results=max_results)
    df = parse_request(feed, query=query, verbose=verbose)
    return df

def helper_remove_dupes(df: pd.core.frame.DataFrame, verbose: int=1) -> pd.core.frame.DataFrame:
    """
    Removes the duplicate entries (checked via URL base) from a given dataframe containing recently fetched queries.

    df -> pd.core.frame.DataFrame
        The given df object containing the parsed data from a query.
    
    verbose -> int
        0: suppresses reporting on count of entry changes to df.
        1: reports on count of entry changes to df.     

    Returns -> pd.core.frame.DataFrame
        A new df containing non-duplicate entries. Ready to be added to the complete_db.csv.

    Example
        unique_df = helper_remove_dupes(df)
    """
    # Check verbose
    if verbose not in {0,1}:
        print(f"Invalid verbose argument: {verbose}. Must be (0,1)")
        return None
    
    if verbose == 1:
        pre_len = len(df)

    # Removing dupes
    database = pd.read_csv("../data/complete_db.csv")
    database = database[database["source"] == "arxiv"]
    checks = database["url"].values.tolist()
    for check in checks:
        df = df[df["url"] != check]
    
    if verbose == 1:
        post_len = len(df)
        print(f"Removed {pre_len - post_len} duplicates ({pre_len} -> {post_len}).")

    # Return
    return df

def fetch_parse_request(query: str=helper.DEFAULT_SEARCH_QUERY, start: int=0, max_results: int=25, verbose: int=1, remove_dupes: int=1) -> list:
    """
    Wrapper that combines both the fetching and parsing of a request. Handles requests larger than 2000. See individual functions for more details.

    query -> str
        The given search query for arxiv to find papers on

    start -> int
        The index of the papers at which to start pulling data on

    max_results -> int
        The total number of papers after `start` to pull from; cannot exceed the value stored in helper.ARXIV_FETCH_LIMIT

    verbose -> int
        0: suppresses all missing-data-points reporting
        1: at the end of script, summarize the total number of missing data points
    
    remove_dupes -> int
        0: does not remove duplicates as part of its fetch
        1: removes duplicates as part of its fetch

    Returns -> pd.core.frame.DataFrame
        The fetch results converted as dataframe.
    """
    # Check verbose
    if verbose not in {0,1}:
        raise ValueError(f"Invalid verbose argument: {verbose}. Must be (0,1)")
    elif remove_dupes not in {0,1}:
        raise ValueError(f"Invalid remove_dupes argument: {remove_dupes}. Must be (0,1). See helper_remove_dupes().")

    # Check query size
    count_of_results = max_results - start + 1
    if count_of_results > helper.ARXIV_VIEW_LIMIT:
        raise ValueError(f"Invalid start and max_result options. You are fetching {count_of_results} results. Arxiv limits to {helper.ARXIV_VIEW_LIMIT}.")

    # Calculate loops
    full_loops = max_results // helper.ARXIV_FETCH_LIMIT
    partial_max_results = max_results - full_loops * helper.ARXIV_FETCH_LIMIT

    # Fetch results
    results = []
    segment_cnt = 1
    for i in range(0, full_loops*helper.MAX_STEP_SIZE, helper.MAX_STEP_SIZE):
        print(f"Fetch/parse segment {segment_cnt}/{full_loops+1}...")
        temp_df = helper_fetch_parse_request(query=query, start=i, max_results=helper.MAX_STEP_SIZE, verbose=verbose)
        results.append(temp_df)
        segment_cnt += 1
    print(f"Fetch/parse segment {segment_cnt}/{full_loops+1}...")
    temp_df = helper_fetch_parse_request(query=query, start=full_loops*helper.MAX_STEP_SIZE, max_results=partial_max_results, verbose=verbose)
    results.append(temp_df)

    if remove_dupes == 1:
        results = [helper_remove_dupes(df) for df in results]
    
    # Return
    return results

def merge_request(list_of_dfs: list, verbose: int=1) -> None:
    """
    Merges the dfs of paper entries into to the completed_db.csv, regardless of whether paper entries are duplicates.

    list_of_dfs -> list
        List of pd.core.frame.DataFrames to merge with completed_db.csv.
    
    verbose -> int
        0: suppresses reporting on count of entry changes to database.
        1: reports on count of entry changes to database. 
    
    Returns -> None
        complete_db.csv is updated with new entries.

    Example
        list_of_dfs = fetch_parse_request()
        merge_request(list_of_dfs)
    """
    # Check verbose
    if verbose not in {0,1}:
        print(f"Invalid verbose argument: {verbose}. Must be (0,1)")
        return None

    if verbose == 1:
            database = pd.read_csv("../data/complete_db.csv")
            super_pre_len = len(database)

    for index, df in enumerate(list_of_dfs):
        print(f"Merging {index+1}/{len(list_of_dfs)}...")
        # Save df
        if verbose == 1:
            database = pd.read_csv("../data/complete_db.csv")
            pre_len = len(database)
            print(f"Attempting to add {len(df)} entries...")

        try:
            df.to_csv("../data/complete_db.csv", mode='a', index=False, header=False)
            print("Saved!")
        except:
            print("Failed to save.")

        if verbose == 1:
            database = pd.read_csv("../data/complete_db.csv")
            post_len = len(database)
            print(f"Added {post_len - pre_len} entries ({pre_len} -> {post_len})!")
    
    if verbose == 1:
        database = pd.read_csv("../data/complete_db.csv")
        super_post_len = len(database)
        print(f"In summary, added {super_post_len - super_pre_len} entries ({super_pre_len} -> {super_post_len})!")

    # return
    return None

def pull_request(query: str=helper.DEFAULT_SEARCH_QUERY, start: int=0, max_results: int=25, verbose: int=1, remove_dupes: int=1) -> None:
    """
    Adds indicated number of paper entries for the given query to the completed_db.csv.

    query -> str
        The given search query for arxiv to find papers on

    start -> int
        The index of the papers at which to start pulling data on

    max_results -> int
        The total number of papers after `start` to pull from

    verbose -> int
        0: suppresses reporting on changes to the database
        1: reports on changes to database

    remove_dupes -> int
        0: does not remove duplicates as part of its fetch
        1: removes duplicates as part of its fetch

    Returns -> None
        complete_db.csv is updated with new entries
    
    Example
        pull_request(query="radiation", max_results=15000, remove_dupes=1)
    """
    print("------PART 1: FETCH PARSE")
    list_of_dfs = fetch_parse_request(query=query, start=start, max_results=max_results, verbose=verbose, remove_dupes=remove_dupes)
    print("------PART 2: MERGE")
    merge_request(list_of_dfs, verbose=verbose)
    return None

def pull_requests(queries: list, start: int=0, max_results: int=25, verbose: int=1, remove_dupes: int=1) -> None:
    """
    Adds indicated number of paper entries for the given queries to the completed_db.csv.

    queries -> list
        The given search queries for arxiv to find papers on, contained in a list

    start -> int
        The index of the papers at which to start pulling data on (for each query)

    max_results -> int
        The total number of papers after `start` to pull from (for each query)

    verbose -> int
        0: suppresses reporting on changes to the database
        1: reports on changes to database

    remove_dupes -> int
        0: does not remove duplicates as part of its fetch
        1: removes duplicates as part of its fetch

    Returns -> None
        complete_db.csv is updated with new entries
    
    Example
        queries = ["radiation", "plasmonics", "stem cell"]
        pull_requests(queries, max_results=15000, remove_dupes=1)
    """
    for query in queries:
        print("--------------------")
        print(f"PULLING {query}.")
        print("--------------------")
        pull_request(query=query, start=start, max_results=max_results, verbose=verbose, remove_dupes=remove_dupes)
        print(f"DONE WITH {query}.")

    return None

#----------------------------------------------------
# Module Checking
#----------------------------------------------------
def main():
    pass

if __name__ == "__main__":
    main()