#!/usr/bin/env python3
'''
    goodXtausch helps to search for books on tauschticket.de using the selected shelves on goodreads.com and returns them as html page.
    A valid goodreads.com API is required, this can be requested for free at https://www.goodreads.com/api
'''

from bs4 import BeautifulSoup
import pandas as pd
from   pathlib import Path
import re
import requests
import time

# api keys
goodreads_api_key = ""

# time delay between requests 
time_delay = 1

# get user input
#goodreads_user_id = input("Goodreads User ID: ")
goodreads_user_id = ''
#goodreads_shelf = input("Goodreads User Shelf: ")
goodreads_shelf = ''

# special characters to remove from search at tauschticket.de
ignore_characters = ['`', '^', '[', ']', '\\', '<']

# fetch books from goodreads
url = "https://www.goodreads.com/review/list" 
params = {
    "v" : 2,
    "id" : goodreads_user_id,
    "shelf" : goodreads_shelf,
    "per_page" : 200,
    "key" : goodreads_api_key,
    "page" : 1
}

def get_title_author(books):
    '''
        gets title and author from the choosen goodreads.com shelf
    '''
    output = []
    for book in books:
        book_data = {
            "title" : book.select_one("title").text.strip(),
            "author" : book.select_one("author").find("name").text
        }
        output.append(book_data)
    return output

def search_tausch(row):
    '''
        search for book(s) at tauschticket.de
    '''
    s = pd.Series(dtype="object")
    
    # get and parse search results
    url = "https://www.tauschticket.de/suche/"
    search_string = "{} {}".format(row["title"], row["author"])
    for char in ignore_characters:
        search_string = search_string.replace(char, "")
    params = {
        "keywords" :  search_string,
        "kategorie" : ""
    }
    resp = requests.get(url, params)
    assert resp.status_code == 200, "Exception accessing tauschticket.de"
    soup = BeautifulSoup(resp.text, "lxml")
    
    # fetch headline
    headline_text = soup.find("div", attrs={"class" : "headline_2_space"}).text
    
    # regular expression is used here to do spacing issues
    if re.search("Keine\s+?Angebote\s+?in", headline_text):
        s["results"] = 0
    elif re.search("Angebote\s+?mit", headline_text):
        pattern = "^(\d+)\s+?Angebote\s+?mit.*?\s+?gefunden"
        result = re.search(pattern, headline_text)
        if result: s["results"] = result.groups()[0]
    else:
        raise Exception("Error parsing headline of tauschticket, perhaps the site has been updated. ")
    
    # save the url
    s["url"] = resp.url
    
    # politely wait
    time.sleep(time_delay)
    return s

def main():
    while True:
        books = []
        resp = requests.get(url, params)
        assert resp.status_code == 200, "Exception accessing Goodreads API. Perhaps it has updated or invalid api key"
        soup = bs4.BeautifulSoup(resp.text, "lxml")
        
        # append results
        books += soup.select("book")
        
        # break if we have reached the end
        end = soup.select_one("reviews").attrs["end"]
        total = soup.select_one("reviews").attrs["total"]
        if end == total: 
            break
        else:
            params["page"] += 1  
        
        # politely wait, following the goodreads terms of service
        time.sleep(time_delay)
   
    # create a pandas series 
    df = pd.DataFrame(data=get_title_author(books))
    
    # pandas operation to apply 
    tausch_df = df.apply(search_tausch, axis=1)
    combined_df = pd.concat([df, tausch_df], axis=1)
    
    # Define path and filename
    base_path   = Path('H:\OneDrive\Programme\_current\goodXtausch')  #adjust
    result_file = base_path / 'output.html'            
    
    # return an html table
    pd.set_option('display.max_colwidth', None)
    combined_df['link'] = "<a href='"+combined_df['url']+"'>"+combined_df['title'].astype(str).str[0:15]+"...</a>"
    html_table = combined_df.to_html(escape=False)
    with open(result_file, "w", encoding="utf-8") as f:
        for line in html_table:
            f.write(line)
            
if __name__  == "__main__":
    main()
