#----------------------------------------------------
# TODO
#----------------------------------------------------
# At fetch for more scopus files, add in NLP preprocessing step here.

#----------------------------------------------------
# Imports
#----------------------------------------------------
import helper
import scopus_scraper

#----------------------------------------------------
# Script
#----------------------------------------------------
helper.load_dotenv() # load environment variables

# API key from environment variable
API_KEY = helper.os.getenv('SCOPUS_API_KEY')
# Scopus API url
SCOPUS_URL = 'https://api.elsevier.com/content/search/scopus'

# Headers for the API request
HEADERS = {
    'Accept': 'application/json',
    'X-ELS-APIKey': API_KEY
}

# Proxies

proxies = {
    'http':'http://130.163.13.200:8080',
    'https':'http://130.163.13.200'
}


# Function to parse data received from API
def parse_data(data, query) -> helper.List[helper.Dict[str, str]]:

    parsed = []

    # Iterate through each entry in the API response
    for field in data.get('search-results', {}).get('entry', []):

        # Extract necessary field from each entry
        title = field.get('dc:title', 'N/A')
        journal = field.get('prism:publicationName', 'N/A')
        doi = field.get('prism:doi', 'N/A')
        authors = field.get('dc:creator', 'N/A') # for author in field.get('author', [])]
        published = field.get('prism:coverDate', 'N/A')
        pii = field.get('pii', "N/A")
        url = 'https://www.sciencedirect.com/science/article/abs/pii/' + str(pii)
        abstract = "N/A" # scopus_scraper.get_abstract(url)
        affiliation_data = field.get('affiliation', [{}])[0]
        country = affiliation_data.get('affiliation-country', 'N/A')
        school = affiliation_data.get('affilname', 'N/A')

        # Add extracted data to the parsed list
        if pii != "N/A" or abstract != "N/A":
            parsed.append({
                'source': 'scopus',
                'query': query, # helper.DEFAULT_SEARCH_QUERY
                'query_time': helper.datetime.now(),
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

def handle_request(writer, query, start, count) -> bool:

    parameters = {
        'query': query,
        'view': 'STANDARD',
        'count': count,
        'start': start
    }
    response = helper.requests.get(SCOPUS_URL, headers=HEADERS, params=parameters) # , verify=False, proxies=proxies

    if response.status_code == 200:
        data = response.json()
        entries = parse_data(data, query)

        for entry in entries:
            writer.writerow(entry)

        helper.time.sleep(helper.random.uniform(1, 2))

    else:
        print("Failed:", response.status_code)
        return False

    return True


def pull_requests(queries, start, max_result) -> None:
    if max_result <= 0:
        print("Invalid value for max_result. Please enter a positive number.")
        return

    data_path = helper.COMPLETE_DATABASE_FILEPATH
    with open(data_path, 'a', newline='', encoding='utf-8') as file:
        writer = helper.csv.DictWriter(file, fieldnames=helper.MASTER_CSV_COLUMNS)

        for query in queries:
            if max_result <= 25:
                if not handle_request(writer, query, start, max_result):
                    break
            else:
                num_iterations = max_result // 25
                for iteration in range(num_iterations):
                    count = 25 if iteration < num_iterations - 1 else max_result % 25
                    if not handle_request(writer, query, 25 * iteration, count):
                        break

        print("Data saved into complete_db.csv")

    


