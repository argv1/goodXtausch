![logo](https://github.com/argv1/goodXtausch/blob/master/images/logo.PNG)
 
## goodXtausch
======================

goodXtausch helps to search for books, games and other items on tauschticket.de based on a goodreads shelf, amazon or steam wishlist and returns the search result for each item as a table in a html page.
 
Since, as of December 8th 2020, Goodreads no longer issues new developer keys for the public developer API and plans to retire the current version of these tools (more info [here](https://help.goodreads.com/s/article/Does-Goodreads-support-the-use-of-APIs)). First approch using selenium is now replaced by a .csv export.
 
![logo](https://github.com/argv1/goodXtausch/blob/master/images/output.PNG)
 
 
## Table of content
 
- [Installation](#installation)
	- [Goodread-Export](#Goodread-Export)
- [Usage](#usage)	
- [License](#license)
- [Outlook](#outlook)
 
## Installation
Windows:
- Download Repo
- Unzip



Optional:
- Create a virtual environment by
```bash
   python -v venv venv
```
- Set Policies:
```bash
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
- Activate Venv:
```bash
   .\venv\Scripts\activate
```


- Install required modules:
```bash
    pip3 install -r requirements.txt
```



*nix:
- Clone repo
```bash
   git clone https://github.com/argv1/goodXtausch.git
```
Optional:
- Create a virtual environment by
```bash
   python3 -v venv venv
```
- Activate Venv:
```bash
   source venv/bin/activate
```
- Install required modules:
```bash
    pip3 install -r requirements.txt
```


### Goodread-Export
 
[How do I export my books?](https://help.goodreads.com/s/article/How-do-I-import-or-export-my-books-1553870934590)
- Follow this link to [Goodreads Import and export](https://www.goodreads.com/review/import)
- Click on "Export Library"
- Download the CSV file and store in the script folder

  
## usage
Run the main.py with the required argument(s)
(Use main.py -h for a list of all options)
 
-a followed by your amazon wishlist url

or

-g for your goodread export file

or

-s followed by your steam UserId

Usage: main.py -a AMAZON_WISHLIST_URL<p>
       main.py -g<p>
       main.py -s STEAM_ID<p>
 
## License
 
This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). 
For more details, please take a look at the [LICENSE file](https://github.com/argv1/goodXtausch/blob/master/LICENSE).
 
 
## outlook
 
- [x] Possibility to use command line
- [x] Possibility to scrap any shelf (here by no further use of the goodreads.com API.)
- [x] Add steam and amazon wishlist
- [x] Creating module for better overview
- [x] goodreads.com scrapping using selenium
- [x] adjusting goodreads.com search using export .csv file
- [ ] more accurate results of the Tauschticket search
- [ ] better handling empty results( due to private wishlists)
- [ ] Add search feature for ISBN (https://www.goodreads.com/api/index#book.show_by_isbn)
- [ ] If ISBN is given for hardcover book, search for additional ISBNs like for the paperback version
