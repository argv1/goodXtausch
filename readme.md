![logo](https://github.com/argv1/goodXtausch/blob/master/images/logo.PNG)
 
## goodXtausch
======================
 
CURRENTLY goodreads not supported due to depricated API keys. Will implement selenium workaround asap.

goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, amazon or steam wishlist and returns the search result for each item as a table in a html page.
 
Since, as of December 8th 2020, Goodreads no longer issues new developer keys for the public developer API and plans to retire the current version of these tools (more info [here](https://help.goodreads.com/s/article/Does-Goodreads-support-the-use-of-APIs)), I desided to use selenium to solve this issue.
 
![logo](https://github.com/argv1/goodXtausch/blob/master/images/output.PNG)
 
 
## Table of content
 
- [Installation](#installation)
    - [User-ID](#User-ID)
	- [Shelf-ID](#Shelf-ID)
- [Usage](#usage)	
- [License](#license)
- [Outlook](#outlook)
 
## Installation
 
You could either use pip
```bash
pip3 install -r requirements.txt
```
 
or pipenv
```bash
pipenv install --ignore-pipfile
```
to install the required packages
 
 
### User-ID
 
Go to the relevant goodreads.com profile to find the corresponding user_id
![User ID](https://github.com/argv1/goodXtausch/blob/master/images/goodreads_user_id.PNG)
 
 
### Shelf-ID
 
![Shelf](https://github.com/argv1/goodXtausch/blob/master/images/goodreads_shelf.PNG)
 
Select one of the available shelves on the left side of the profile page.
  
## usage
Run the main.py with the required argument(s)
(Use main.py -h for a list of all options)
 
-a followed by your amazon wishlist url

or

-s followed by the goodreads.com shelf and
-p followed by the corresponding goodreads.com profile

or

-u followed by your steam UserId

Usage: main.py -u STEAM_ID<p>
 
## License
 
This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). 
For more details, please take a look at the [LICENSE file](https://github.com/argv1/goodXtausch/blob/master/LICENSE).
 
 
## outlook
 
- [x] Possibility to use command line
- [x] Possibility to scrap any shelf (here by no further use of the goodreads.com API.)
- [x] Add steam and amazon wishlist
- [x] Creating module for better overview
- [ ] goodreads.com scrapping using selenium
- [ ] more accurate results of the Tauschticket search
- [ ] better handling empty results( due to private wishlists)
- [ ] Add search feature for ISBN (https://www.goodreads.com/api/index#book.show_by_isbn)
- [ ] If ISBN is given for hardcover book, search for additional ISBNs like for the paperback version
