from bs4 import BeautifulSoup
import requests

def get_abstract(url) -> str:

    # Set headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    target_div = soup.find('div', class_="abstract author") # div where the abstract is located
    if target_div is not None:
        target_p = target_div.find('p') # the abstract text
        if target_p is not None:
            return target_p.text

    return "N/A"
