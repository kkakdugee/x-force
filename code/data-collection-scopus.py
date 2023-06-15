from dotenv import load_dotenv # Loading environment variables (API KEY)
from typing import List, Dict 

import requests # HTTP requests
import csv # Creating and Manipulating CSV files
import os 
import helper


load_dotenv() # load environment variables

# API key from environment variable
API_KEY = os.getenv('SCOPUS_API_KEY')
# Scopus API url
SCOPUS_URL = 'https://api.elsevier.com/content/search/scopus'

# Headers for the API request
HEADERS = {
    'Accept': 'application/json',
    'X-ELS-APIKey': API_KEY
}

# Function to parse data received from API
def parse_data(data) -> List[Dict[str, str]]:

    parsed = []

    # Iterate through each entry in the API response
    for field in data.get('search-results', {}).get('entry', []):

        # Extract necessary field from each entry
        title = field.get('dc:title', 'N/A')
        authors = field.get('dc:creator', 'N/A') # for author in field.get('author', [])]
        year = field.get('prism:coverDate', 'N/A')[:4]
        abstract = field.get('dc:description', 'N/A')
        url = 'https://www.sciencedirect.com/science/article/abs/pii/' + str(field.get('pii'))
        citations = field.get('citedby-count', 'N/A')
        affiliation_data = field.get('affiliation', [{}])[0]
        country = affiliation_data.get('affiliation-country', 'N/A')
        school = affiliation_data.get('affilname', 'N/A')

        # Add extracted data to the parsed list
        parsed.append({
            'title': title,
            'authors': authors, # ', '.join(authors),
            'schools': school,
            'countries': country,
            'year of publication': year,
            'abstract text': abstract,
            'url': url,
            'citation count': citations
        })
    
    return parsed

# Function to search Scopus API
def search() -> None:

    # Get search terms from user
    # query = input("Enter search terms separated by commas: ").split(",")
    
    # Define parameters for API request
    parameters = {
        'query': helper.SEARCH_QUERY,
        'view': 'STANDARD', # COMPLETE
        'count': 25
    }

    # Make the API request
    response = requests.get(SCOPUS_URL, headers=HEADERS, params=parameters)
    
    # If the request is successful, parse data and write to csv
    if response.status_code == 200:
        data = response.json()
        # print(data)
        with open(f'./data/{helper.SEARCH_QUERY}.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=helper.MASTER_CSV_COLUMNS)
            writer.writeheader()
            writer.writerows(parse_data(data))
        print(f"Data saved into {helper.SEARCH_QUERY}.csv")
    else:
        print("Failed:", response.status_code)
    

if __name__ == "__main__":
    search()


