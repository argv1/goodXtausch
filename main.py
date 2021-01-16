#!/usr/bin/env python3
'''
    goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, 
    amazon or steam wishlist and returns the search result for each item as a table in a html page.
    
'''
import argparse
from goodXtausch import *
import pandas as pd
import sys

# Global settings
time_delay = 1

def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--amazon', help='Enter (public accessable) amazon wishlist url', type=str)
    group.add_argument('-s', '--shelf', help='Enter enter name of the shelf', type=str) 
    group.add_argument('-p', '--user_id', help='Enter enter correspondent goodreads user id', type=str)
    group.add_argument('-u', '--steam_id', help='Enter steam id', type=str)
    args = parser.parse_args()

    if (args.amazon):
        ama_wlist   = args.amazon
        df = pd.DataFrame(data=get_amazon_items(ama_wlist), columns=["title"])
        mode = "a"
    elif(args.shelf and args.user_id):
        goodreads_shelf   = args.shelf
        goodreads_user_id = args.user_id
        df = pd.DataFrame(data=get_books(goodreads_shelf, goodreads_user_id, time_delay))
        mode = "b"
    elif(args.steam_id):
        steam_id = args.steam_id
        df = pd.DataFrame(data=get_games(steam_id), columns=["title"])
        mode = "s"
    else:
        print("Missing arguments, please run main.py -h for help")
        sys.exit(1)

    # search tauschticket for the desired items
    tausch_df = df.apply(search_tausch, args=(mode, time_delay), axis=1)
    combined_df = pd.concat([df, tausch_df], axis=1)

    # return an html table
    get_html(combined_df)
         
if __name__  == "__main__":
    main()