from   bs4 import BeautifulSoup
import goodXtausch as gXt
import requests

def get_amazon_items(wishlist, user_agent_f):
    '''
        grab items from the choosen public accessable amazon wishlist
    '''
    output, headers = [], gXt.get_random_user_agent(user_agent_f)

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