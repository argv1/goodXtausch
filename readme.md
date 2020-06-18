![logo](https://github.com/argv1/goodXtausch/blob/master/images/logo.PNG)

## goodXtausch
======================

goodXtausch helps to search for books on tauschticket.de using the selected shelves on goodreads.com and returns them as html page.


## Table of content

- [Installation](#installation)

- [Setup](#setup)
    - [API-key](#API-key)
    - [User-ID](#User-ID)
	- [Shelf-ID](#Shelf-ID)
- [Usage](#usage)	
- [License](#license)
- [Outlook](#outlook)

## Installation

goodXtausch use the packaging tool Pipenv.
If you are not already use Pipenv, please run 
```bash
pip install pipenv
```

After you successful installed pipenv, please run
```bash
pipenv install --ignore-pipfile
```
to install the required packages

## setup

### API-key

1. Register for a free [Goodreads API key](https://www.goodreads.com/api/keys) in order to access your list of books.
2. Ensure your [Goodreads account privacy settings](https://www.goodreads.com/user/edit?tab=settings) allow for access to your shelves via the API.
    - Set `Who can view my profile:` to `anyone (including search engines)`
    - Check the box `Allow partners of Goodreads to display my reviews`


Enter this api key here:
```python
goodreads_api_key = YOUR-API-KEY
```

### User-ID

Browser to your goodreads.com profile to find your user_id
![User ID](https://argv1.github.com/goodXtausch/images/goodreads_user_id.PNG)

Enter your user_id here:
```python
goodreads_user_id = 'YOUR-USER-ID'
```

### Shelf-ID

You can find your shelfs on the left side of your profile page
![Shelf](https://argv1.github.com/goodXtausch/images/goodreads_shelf1.PNG)

Choose one of them and enter it here:
```python
goodreads_shelf = 'YOUR-SHELF'
```

## usage
After you entered the above information, run the main.py and enjoy the output.html file with the results for your desired books.

## License

This code is licensed under the [GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/). 
For more details, please take a look at the [LICENSE file](https://github.com/argv1/goodXtausch/blob/master/LICENSE).


## outlook

- Possibility to enter user_id and shelf on the command line
- Add search feature for ISBN (https://www.goodreads.com/api/index#book.show_by_isbn)
- If ISBN is given for hardcover book, search for additional ISBNs like for the paperback version
