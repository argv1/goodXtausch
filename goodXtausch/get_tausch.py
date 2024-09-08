from   bs4 import BeautifulSoup as bs
import pandas as pd
import re
import requests
import time


def clean_string(search_string):
    # Erlaubt nur Buchstaben, Zahlen, Leerzeichen, Anführungszeichen und Bindestriche
    cleaned_string = re.sub(r'[^a-zA-Z0-9äÄöÖüÜßéèêÉÈÊëËçÇàÀâÂôÔûÛùÙ\s\"\'-]', '', search_string)
    return cleaned_string

def get_tausch(row, mode, time_delay, logger):
    '''
        search for item(s) at tauschticket.de
    '''
    s = pd.Series(dtype="object")
    
    # get and parse search results
    url = "https://www.tauschticket.de/suche/"
    if(mode == "g"):
        search_string = f'{row["title"]} {row["Author"]}'
    else:
        search_string = f'{row["title"]}'
    
    search_term = clean_string(search_string)
    
    params = {
            "keywords" :  search_term,
            "kategorie" : ""
        }
    if(mode == "g"):
        params.update({"kategorie" : "buch"})
    elif(mode == "s"):
        params.update({"kategorie" : "pcgame"})
  
    resp = requests.get(url, params=params)
    assert resp.status_code == 200, "Exception accessing tauschticket.de"
    soup = bs(resp.text, "lxml")
    
    # fetch headline
    headline_text = soup.find("div", attrs={"class" : "headline_2_space"}).text
    
    # Older Version of tauschticket replied with Keine Angebote instead of 0 Angebote
    # Regex pattern to match the search result headline
    pattern = r'(\d+)\s+Angebote(?:\s+in\s+([^\"]+))?\s+mit\s+\"([^\"]+)\"\s+gefunden$'
    result = re.search(pattern, headline_text)
    
    if result:
        s["results"] = int(result.group(1))
        s["search_term"] = result.group(3)
        s["category"] = result.group(2) if result.group(2) else "allgemein"
        s["url"] = resp.url

    else:
        logger.warning(f"Error parsing headline of tauschticket:\n{headline_text}")

    # politely wait
    time.sleep(time_delay)
    return s