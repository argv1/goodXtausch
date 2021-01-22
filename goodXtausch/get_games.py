import goodXtausch as gXt
import json
import requests

def steam(steam_id, user_agent_f):
    '''
        gets games from the choosen player ids steam wishlist 
        (need to be public available)
    '''
    output, headers, n = [], gXt.get_random_user_agent(user_agent_f), 0
    steam_url = f'https://store.steampowered.com/wishlist/profiles/{steam_id}/wishlistdata/?p='

    # Loop is required for wishlists with more than 100 items
    while True:
        data = requests.get(steam_url + str(n), headers=headers).json()
        # if new page contains additional items, add rge name to the list
        if len(data) > 0:
            output.extend(value['name'] for value in data.values())
            n+=1
        else:
            break
    return output