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
sys.path.append("Modules/")
import helper
import arxiv

#----------------------------------------------------
# Main
#----------------------------------------------------
def main():
    print("Welcome!")

    while True:
        print("Menu")
        print("-----")
        print("1. Update database by search term")
        print("2. Visualizations by search term")
        print("3. Summary of database")
        print("4. Clean dupes from database")
        print("5. Exit program")
        print("0. Wipe database")
        user_input = input("Pick your option (1-5, 0).")
        if user_input not in {"0","1","2","3","4","5"}:
            print("Invalid answer. Please input an integer from this list (1-5, 0).", end="\n")
        else:
            break
    if user_input == 1:
        print("1")
        return None
        # arvix_scripts.pull_requests()
    elif user_input == 2:
        print("2")
        return None
    elif user_input == 3:
        print("3")
        return None
    elif user_input == 4:
        print("4")
        return None
    elif user_input == 5:
        print("5")
        return None
    elif user_input == 0:
        print("0")
        return None


if __name__ == "__main__":
    main()