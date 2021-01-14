#!/usr/bin/env python3
'''
    goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, 
    amazon or steam wishlist and returns the search result for each item as a table in a html page.
    
'''
import argparse
from   bs4 import BeautifulSoup
import pandas as pd
from   pathlib import Path
import random
import re
import requests
import time
import sys

# Global settings
base_path = Path(__file__).parent.absolute()
user_agent_f = base_path / 'random_user_agent.csv'  
result_f = base_path / 'output.html'   
time_delay = 1

def get_random_user_agent():
    '''
        grab a random user agent, based on https://github.com/argv1/random_user_agent
    '''   
    with open(user_agent_f, "r") as f:
        lines = f.read().splitlines()
        lines.pop(0)
    return({'User-Agent': random.choice(lines).rsplit(',', 3)[0]})

def get_items(wishlist):
    '''
        grab items from the choosen public accessable amazon wishlist
    '''
    output, headers = [], get_random_user_agent()

    # fetch the url
    r = requests.get(wishlist, headers=headers)
    soup = BeautifulSoup(r.content, "lxml")

    # Focus in the right div
    soup = soup.find(id="content-right")

    # get title from a class
    links = soup.find_all('a', {'class': 'a-link-normal'})
    for link in links:
        if link.get('title') != None:
            output.append(link.get('title'))

    # remove duplicates
    output =list(dict.fromkeys(output))
    return output

def get_games(steam_id):
    '''
        gets games from the choosen player ids steam wishlist
    '''
    import json

    output, headers, n = [], get_random_user_agent(), 0
    steam_url = f'https://store.steampowered.com/wishlist/profiles/{steam_id}/wishlistdata/?p='

    # fetch the url
    r = requests.get(steam_url, headers=headers)
    soup = BeautifulSoup(r.text, features="lxml")

    # Loop is required for wishlists with more than 100 items
    while True:
        data = requests.get(steam_url + str(n)).json()

        # if new page contains additional items, add rge name to the list
        if len(data) > 0:
            output.extend(value['name'] for value in data.values())
            n+=1
        else:
            break
    return output

def get_books(goodreads_shelf, goodreads_user_id):
    '''
        scrap all books from selected shelf and afterwards store the title and author for each item
    '''
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys 

    browser = base_path / 'chromedriver.exe'  
    # fetch books from goodreads
    url = "https://www.goodreads.com/review/list" 
    params = {
        "v" : 2,
        "id" : goodreads_user_id,
        "shelf" : goodreads_shelf,
        "per_page" : 200,
        "key" : "depricated_api_key", #ändern
        "page" : 1
    }

    # some user agent headers
    books, headers = [], get_random_user_agent()

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

def search_tausch(row, setting):
    '''
        search for book(s) at tauschticket.de
    '''
    # special characters to remove from search at tauschticket.de
    ignore_characters = ['`', '^', '[', ']', '\\', '<', '–', '™']  #, '®', '-'

    s = pd.Series(dtype="object")
    
    # get and parse search results
    url = "https://www.tauschticket.de/suche/"
    if(setting == "b"):
        search_string = f'{row["title"]} {row["author"]}'
    else:
        search_string = f'{row["title"]}'
    for char in ignore_characters:
        search_string = search_string.replace(char, "")
    
    params = {
            "keywords" :  search_string,
            "kategorie" : ""
        }
    if(setting == "b"):
        params.update({"kategorie" : "buch"})
    elif(setting == "s"):
        params.update({"kategorie" : "pcgame"})
  
    resp = requests.get(url, params=params)
    assert resp.status_code == 200, "Exception accessing tauschticket.de"
    soup = BeautifulSoup(resp.text, "lxml")
    
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

def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--amazon', help='Enter (public accessable) amazon wishlist url', type=str)
    group.add_argument('-s', '--shelf', help='Enter enter name of the shelf', type=str) 
    group.add_argument('-p', '--user_id', help='Enter enter your goodreads user id', type=str) # user id needs to correspondent to provided shelf
    group.add_argument('-u', '--steam_id', help='Enter steam id', type=str)
    args = parser.parse_args()

    if (args.amazon):
        ama_wlist   = args.amazon
        df = pd.DataFrame(data=get_items(ama_wlist), columns=["title"])
        setting = "a"
    elif(args.shelf and args.user_id):
        goodreads_shelf   = args.shelf
        goodreads_user_id = args.user_id
        df = pd.DataFrame(data=get_books(goodreads_shelf, goodreads_user_id))
        setting = "b"
    elif(args.steam_id):
        steam_id = args.steam_id
        df = pd.DataFrame(data=get_games(steam_id), columns=["title"])
        setting = "s"
    else:
        print("Missing arguments, please run main.py -h for help")
        sys.exit(1)

    # pandas operation to apply 
    tausch_df = df.apply(search_tausch, args=(setting), axis=1)
    combined_df = pd.concat([df, tausch_df], axis=1)
    
    # return an html table
    pd.set_option('display.max_colwidth', None)
    combined_df['link'] = "<a href='"+combined_df['url']+"'>"+combined_df['title'].astype(str).str[0:15]+"...</a>"
    html_table = combined_df.to_html(escape=False)
    with open(result_f, "w", encoding="utf-8") as f:
        for line in html_table:
            f.write(line)
            
if __name__  == "__main__":
    main()