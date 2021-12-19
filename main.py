#!/usr/bin/env python3
'''
    goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, 
    amazon or steam wishlist and returns the search result for each item as a table in a html page.
    
'''
import argparse
import goodXtausch as gXt
import pandas as pd
from   pathlib import Path
import sys

# Global settings
time_delay = 1
base_path = Path(__file__).parent.absolute()
user_agent_f = base_path / 'random_user_agent.csv' 
config_f = base_path / 'config.ini'
result_f = base_path / 'output.html'


def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--amazon', help='Enter (public accessable) amazon wishlist url', type=str)
    group.add_argument('-g', '--goodreads', help='Enter export.csv filename', type=str, default="goodreads_library_export.csv") 
    group.add_argument('-s', '--steam_id', help='Enter steam id', type=str)
    args = parser.parse_args()

    if (args.amazon):
        mode = "a"
        ama_wlist   = args.amazon
        df = pd.DataFrame(data=gXt.get_amazon_items(ama_wlist, user_agent_f), columns=["title"])
    elif(args.goodreads):
        mode = "g"        
        goodreads_shelf_export_f = base_path / args.goodreads
        df = pd.DataFrame(data=gXt.goodreads(goodreads_shelf_export_f))
    elif(args.steam_id):
        mode = "s"
        steam_id = args.steam_id
        df = pd.DataFrame(data=gXt.steam(steam_id, user_agent_f), columns=["title"])
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