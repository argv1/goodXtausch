#!/usr/bin/env python3
'''
    goodXtausch helps to search for books on tauschticket.de using the selected shelves on goodreads.com and returns them as html page.
    A valid goodreads.com API is required, this can be requested for free at https://www.goodreads.com/api
'''
import argparse
from bs4 import BeautifulSoup
import pandas as pd
from   pathlib import Path
import random
import re
import requests
import time

# api keys
goodreads_api_key = "YOUR_API_KEY"

# time delay between requests 
time_delay = 1

def get_books(goodreads_shelf, goodreads_user_id):
    '''
        scrap all books from selected shelf and afterwards store the title and author for each item
    '''
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
    # some user agent headers
    user_agent_list = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    ]
    
    #Select random header
    headers = {'User-Agent': random.choice(user_agent_list)}

    books = []

    while True:
        resp = requests.get(url, params)
        assert resp.status_code == 200, "Exception accessing Goodreads API. Perhaps it has updated or invalid api key"
        soup = BeautifulSoup(resp.text, "lxml")
        
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

    # get author and title for each book
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
    # special characters to remove from search at tauschticket.de
    ignore_characters = ['`', '^', '[', ']', '\\', '<', '–', '™']]

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
    # Initiate the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--shelf', help='Enter enter name of the shelf', type=str, required=True) 
    parser.add_argument('-u', '--user_id', help='Enter enter your goodreads user id', type=str, required=True) # user id needs to correspondent to goodreads api key owner
    args = parser.parse_args()
    goodreads_shelf   = args.shelf
    goodreads_user_id = args.user_id
   
    # create a pandas series 
    df = pd.DataFrame(data=get_books(goodreads_shelf, goodreads_user_id))
    
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
