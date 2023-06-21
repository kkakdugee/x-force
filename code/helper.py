#----------------------------------------------------
# arXiv API Defaults
#----------------------------------------------------
DEFAULT_BASE_URL = "https://export.arxiv.org/api/"
DEFAULT_METHOD = "query"
DEFAULT_URL = DEFAULT_BASE_URL + DEFAULT_METHOD
DEFAULT_SEARCH_QUERY = "radiation"
DEFAULT_DATE_QUERY = "2010-01-01" # year-mo-day
MAX_STEP_SIZE = 2000
MAX_VIEW_SIZE = 30000
MIN_WAIT_TIME = 3 # seconds
DEFAULT_PARAMS = {"search_query": DEFAULT_SEARCH_QUERY,
                  "sortBy": 'submittedDate',
                  "sortOrder": 'ascending',
                  "start": 0,
                  "max_results": 5
                  }

#----------------------------------------------------
# arXiv Data Extract Defaults
#----------------------------------------------------
ARXIV_KEYS = ["title", 
              "arxiv_journal_ref", 
              "authors", 
              "arxiv_doi", 
              "published", 
              "summary", 
              "link", 
              "tags"
              ]

MASTER_CSV_COLUMNS = ["title",
                      "journal",
                      "authors",
                      "doi",
                      "published",
                      "abstract",
                      "url",
                      "tags"
                      ]

META_CSV_COLUMNS = ["query",
                    "target_date_paper_url",
                    "target_date_paper_title",
                    "target_date_paper_publish_date",
                    "start_index",
                    "target_date",
                    "date_of_last_index_extraction"
                    ]