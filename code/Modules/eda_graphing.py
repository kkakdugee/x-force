#----------------------------------------------------
# Imports Checking
#----------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import feedparser
import time
from datetime import datetime
import sys
import helper

#----------------------------------------------------
# Graphing Class
#----------------------------------------------------
class XForce_Grapher():
    def __init__(self) -> None:
        self._data = None
        self._sources = None
        self._queries = None
        self.load("./data/complete_db.csv")
        return None


    def peek_data(self):
        return self._data.head()

    def get_data(self):
        return self._data
    

    def get_sources(self):
        return self._sources
    

    def get_queries(self):
        return self._queries


    def set_data(self, path: str) -> None:
        self.load(path)
        return None


    def load(self, path: str) -> None:
        df = pd.read_csv(path)
        sources = list(set(df["source"].values.tolist()))
        sources.append("ALL")
        queries = list(set(df["query"].values.tolist()))

        self._data = df
        self._sources = sources
        self._queries = queries
        return None


    def graph_freq(self, query: str, source: str="ALL") -> None:
        """
        Graphs the publishing frequency of papers in the database.

        query -> str
            The given search query to visualize

        source -> int
            The database source to restrict visualizations on
            arxiv: Graph only results from arxiv
            scopus: Graph only results from scopus
            ALL: Graphs all

        Returns -> None
            Prints out matplotlib graph of the published frequen
        
        Example
            graph_freq("radiation", "arxiv")
        """
        if source not in self._sources:
            print(f"{source} not found. Available options are {self._sources}, where 'ALL' analyzes from all sources.")
            return None

        df = self._data
        if source != "ALL":
            df = df[df["source"] == source]
        df = df[df["query"] == query]
        dates_extract = df["published"].apply(lambda x: x.split('T')[0])
        dates = [datetime(int(i.split("-")[0]), int(i.split("-")[1]), int(i.split("-")[2])) for i in dates_extract]
        
        plt.title(f"Source: {source}, Query: {query}")
        plt.suptitle(f"Publish Frequency within {len(dates)} Most Recent Papers")
        plt.xlabel("Publish Dates")
        plt.ylabel("Frequency")
        plt.grid("True")
        plt.xticks(rotation=45)
        plt.hist(dates, 25, alpha=.75)
        plt.show()
        return None
    
#----------------------------------------------------
# Module Checking
#----------------------------------------------------
def main():
    return None

if __name__ == "__main__":
    main()