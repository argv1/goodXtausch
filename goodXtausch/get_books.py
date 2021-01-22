from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sys
import time

class Goodbot():
    def __init__(self, username, password, browser, time_delay):
        self.driver = webdriver.Chrome(executable_path=browser)
        self.driver.maximize_window()
        self.username = username
        self.__password = password
        self.time_delay = time_delay

    def __good_login(self):
        try:
            self.driver.get("https://www.goodreads.com/")
            time.sleep(self.time_delay)
            username_field = self.driver.find_element(By.ID, "userSignInFormEmail")
            username_field.clear()
            username_field.send_keys(self.username)

            password_field = self.driver.find_element(By.ID, "user_password")
            password_field.clear()
            password_field.send_keys(self.__password)
            time.sleep(self.time_delay)
            password_field.submit()
        except:
            print("Login to goodreads.com not possible.")
            sys.exit(1)

    def scroll(self):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.time_delay)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

    def get_books(self, goodreads_url):
        self.__good_login()
        self.driver.get(goodreads_url)
        time.sleep(self.time_delay)
        self.scroll()
        soup = bs(self.driver.page_source, 'lxml')
        self.driver.close()

        titles = [re.search(r'\s+(.*)\n',td.find('a').text).group(1) for td in soup.find_all('td' , class_='field title')]
        authors = [td.find('a').text for td in soup.find_all('td' , class_='field author')]
        
        output, n = [], 0

        for title in titles:
            book_data = {
                "title" : title,
                "author" : authors[n]
            }
            n+=1
            output.append(book_data)
        return output