#!/usr/bin/env python3
'''
    goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, 
    amazon or steam wishlist and returns the search result for each item as a table in a html page.
    
'''
import argparse
from configparser import ConfigParser
from getpass import getpass
import goodXtausch as gXt
import pandas as pd
from   pathlib import Path
import sys

# Global settings
time_delay = 1
base_path = Path(__file__).parent.absolute()
user_agent_f = base_path / 'random_user_agent.csv'  
browser = base_path / 'chromedriver.exe' 
config_f = base_path / 'config.ini'
result_f = base_path / 'output.html'

def credentials():
    # get credentials
    config_file = ConfigParser()
    config_file.read(config_f)
    settings = config_file['SETTINGS']
    try:
        username = settings['Username']
    except KeyError:
        username = input('[?] Goodreads Username: ')
    try:
        password = settings['Password']
    except KeyError:
        password = getpass(f'[?] Goodreads Password for {username}: ')
    return username, password

def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--amazon', help='Enter (public accessable) amazon wishlist url', type=str)
    group.add_argument('-g', '--goodreads', help='Enter ID-SELF', type=str) 
    group.add_argument('-s', '--steam_id', help='Enter steam id', type=str)
    args = parser.parse_args()

    if (args.amazon):
        ama_wlist   = args.amazon
        df = pd.DataFrame(data=gXt.get_amazon_items(ama_wlist, user_agent_f), columns=["title"])
        mode = "a"
    elif(args.goodreads):
        username, password = credentials()
        goodreads_user_id, goodreads_shelf = args.goodreads.split("-")
        goodreads_url = f"https://www.goodreads.com/review/list/{goodreads_user_id}?utf8=%E2%9C%93&shelf={goodreads_shelf}&per_page=infinite"
        goodreads = gXt.Goodbot(username, password, browser, time_delay)
        df = pd.DataFrame(data=goodreads.get_books(goodreads_url))
        mode = "g"
    elif(args.steam_id):
        steam_id = args.steam_id
        df = pd.DataFrame(data=gXt.steam(steam_id, user_agent_f), columns=["title"])
        mode = "s"
    else:
        print("Missing arguments, please run main.py -h for help")
        sys.exit(1)

    # search tauschticket for the desired items
    tausch_df = df.apply(gXt.get_tausch, args=(mode, time_delay), axis=1)

    combined_df = pd.concat([df, tausch_df], axis=1)

    # return an html table
    gXt.get_html(combined_df, result_f)

if __name__  == "__main__":
    main()