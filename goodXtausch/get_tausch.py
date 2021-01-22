from   bs4 import BeautifulSoup as bs
import pandas as pd
import re
import requests
import time

def get_tausch(row, mode, time_delay):
    '''
        search for item(s) at tauschticket.de
    '''
    # special characters to remove from search at tauschticket.de
    ignore_characters = ['`', '^', '[', ']', '\\', '<', '–', '™']  #, '®', '-'

    s = pd.Series(dtype="object")
    
    # get and parse search results
    url = "https://www.tauschticket.de/suche/"
    if(mode == "g"):
        search_string = f'{row["title"]} {row["author"]}'
    else:
        search_string = f'{row["title"]}'
    for char in ignore_characters:
        search_string = search_string.replace(char, "")
    
    params = {
            "keywords" :  search_string,
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
    
    # regular expression is used here to do spacing issues
    if re.search("Keine\s+?Angebote\s+?in", headline_text):
        s["results"] = 0
    elif re.search("Angebote.*?mit", headline_text):
        pattern = "^(\d+)\s+?Angebote.*?mit.*?\s+?gefunden"
        result = re.search(pattern, headline_text)
        if result: 
            s["results"] = result.groups()[0]
    else:
        raise Exception("Error parsing headline of tauschticket, perhaps the site has been updated.")
    
    # save the url
    s["url"] = resp.url
    
    # politely wait
    time.sleep(time_delay)
    return s