#----------------------------------------------------
# TODO
#----------------------------------------------------
# At fetch for more arxiv files, add in NLP preprocessing step here.

#----------------------------------------------------
# Imports
#----------------------------------------------------
import helper

#----------------------------------------------------
# Script
#----------------------------------------------------
def get_abstract(url) -> str:

    proxies = {
        'http':'http://130.163.13.200:8080',
        'https':'http://130.163.13.200:8080'
    }

    # Set headers to mimic a browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    response = helper.requests.get(url, headers=headers, verify=False, proxies=proxies)
    soup = helper.BeautifulSoup(response.text, 'html.parser')

    target_div = soup.find('div', class_="abstract author") # div where the abstract is located
    if target_div is not None:
        target_p = target_div.find('p') # the abstract text
        if target_p is not None:
            return target_p.text

    return "N/A"
