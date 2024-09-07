#!/usr/bin/env python3
'''
    goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, 
    amazon or steam wishlist and returns the search result for each item as a table in a html page.
    
'''
import argparse
from configparser import ConfigParser
import goodXtausch as gXt
import logging
import pandas as pd
from   pathlib import Path
import webbrowser
import sys

def main():
    # Initiate the parser
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--amazon', help='Enter (public accessable) amazon wishlist url', type=str)
    group.add_argument('-g', '--goodreads', help='Enter export.csv filename', type=str) 
    group.add_argument('-s', '--steam_id', help='Enter steam id', type=str)
    parser.add_argument('-o', '--output', help='Specify output file', type=str, default="output.html")
    args = parser.parse_args()

    result_f = base_path / args.output

    if [args.amazon, args.goodreads, args.steam_id].count(None) == 1:
        logger.warning("Bitte genau ein Argument für Amazon, Goodreads oder Steam übergeben.")
        sys.exit(1)

    if (args.amazon):
        mode = "a"
        ama_wlist   = args.amazon
        try:
            df = pd.DataFrame(data=gXt.get_amazon_items(ama_wlist, user_agent_f), columns=["title"])
        except Exception as e:
            logger.warning(f"Fehler beim Abrufen der Amazon-Wunschliste: {e}")
            sys.exit(1)
    elif(args.goodreads):
        mode = "g"        
        goodreads_shelf_export_f = base_path / args.goodreads
        if not goodreads_shelf_export_f.exists():
            logger.warning(f"Datei {goodreads_shelf_export_f} nicht gefunden.")
            sys.exit(1)
        
        try:
            df = pd.DataFrame(data=gXt.goodreads(goodreads_shelf_export_f))
        except Exception as e:
            logger.warning(f"Fehler beim Verarbeiten der Goodreads-Exportdatei: {e}")
            sys.exit(1)
    elif(args.steam_id):
        mode = "s"
        steam_id = args.steam_id
        try:
            df = pd.DataFrame(data=gXt.steam(steam_id, user_agent_f), columns=["title"])
        except Exception as e:
            logger.warning(f"Fehler beim Abrufen der Steam-Wunschliste: {e}")
            sys.exit(1)
    else:
        logger.warning("Missing arguments, please run main.py -h for help")
        sys.exit(1)

    # search tauschticket for the desired items
    tausch_df = df.apply(lambda row: gXt.get_tausch(row, mode, time_delay, logger), axis=1)

    combined_df = pd.concat([df, tausch_df], axis=1)

    # Sort the combined DataFrame by 'results' (descending) and then by 'category' (descending)
    sorted_df = combined_df.sort_values(by=['results', 'category'], ascending=[False, False])

    # return an html table
    gXt.get_html(sorted_df, result_f)

    # Opens result in your webbrowser
    webbrowser.open(f"file://{result_f}")

if __name__  == "__main__":
    base_path = Path(__file__).parent.absolute()

    # Config.ini initialisieren
    config_path = base_path / 'config.ini'
    config_f = ConfigParser()

    if not config_path.exists():
        print(f"Datei {config_f} nicht gefunden.")
        sys.exit(1)

    config_f.read(config_path)


    # Setup Logging
    log_file = config_f.get('Output', 'logging')

    # Konvertiere log_file in ein Path-Objekt
    log_file_path = Path(log_file)


    if not log_file_path.exists():
        print(f"Datei {log_file_path} nicht gefunden.")
        sys.exit(1)

    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)

    # create log file handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # create stream handler (console output)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    # set format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # initialize
    logger.info(f"Logger initialized. Log file {log_file} is being saved to {log_file_path}")

    # Global settings
    time_delay = 1

    user_agent_f = base_path / 'random_user_agent.csv' 
    if not user_agent_f.exists():
        logger.warning(f"Datei {user_agent_f} nicht gefunden.")
        sys.exit(1)

    main()