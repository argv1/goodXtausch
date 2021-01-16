from   bs4 import BeautifulSoup
from goodXtausch import get_random_user_agent
from   pathlib import Path
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Global settings
base_path = Path(__file__).parent.absolute()
browser = base_path / 'chromedriver.exe' 

def get_books(goodreads_shelf, goodreads_user_id, time_delay):
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