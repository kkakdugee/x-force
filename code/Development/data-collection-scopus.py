from dotenv import load_dotenv # Loading environment variables (API KEY)
from typing import List, Dict 

import requests # HTTP requests
import csv # Creating and Manipulating CSV files
import os # For accessing the env file
import time # Wait time
import random 

# Helper modules
sys.path.insert(0, "../Modules")
import helper
import scopus_scraper


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
        journal = field.get('prism:aggregationType', 'N/A')
        doi = field.get('prism:doi', 'N/A')
        authors = field.get('dc:creator', 'N/A') # for author in field.get('author', [])]
        published = field.get('prism:coverDate', 'N/A')[:4]
        pii = field.get('pii', "N/A")
        url = 'https://www.sciencedirect.com/science/article/abs/pii/' + str(pii)
        abstract = scopus_scraper.get_abstract(url)

        affiliation_data = field.get('affiliation', [{}])[0]
        country = affiliation_data.get('affiliation-country', 'N/A')
        school = affiliation_data.get('affilname', 'N/A')

        # Add extracted data to the parsed list
        if pii != "N/A" or abstract != "N/A":
            parsed.append({
                'title': title,
                'journal': journal,
                'doi': doi,
                'authors': authors,
                'published': published,
                'abstract': abstract,
                'url': url,
                'tags': {
                    'country': country,
                    'school': school
                }
            })
    
    return parsed

# Function to search Scopus API
def gather_data() -> None:

    # Define parameters for API request
    parameters = {
        'query': helper.SEARCH_QUERY,
        'view': 'STANDARD', # COMPLETE
        'count': 25,
        'start': 0
    }

    seen_dois = set()

    data_path = './data/scopus.csv'

    with open(data_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=helper.MASTER_CSV_COLUMNS)
        
        # Check if the file is empty or doesn't exist, then write headers
        if os.stat(data_path).st_size == 0:
            writer.writeheader()
        
        while parameters['start'] != 75:
            response = requests.get(SCOPUS_URL, headers=HEADERS, params=parameters)
            if response.status_code == 200:
                data = response.json()
                entries = parse_data(data)
                
                for entry in entries:
                    if entry['doi'] not in seen_dois:
                        writer.writerow(entry)
                        seen_dois.add(entry['doi'])
                        
                parameters['start'] += 25
                time.sleep(random.uniform(1, 3))
            else:
                print("Failed:", response.status_code)
                break

        file.close()

    print(f"Data saved into scopus.csv")

    

if __name__ == "__main__":
    gather_data()


