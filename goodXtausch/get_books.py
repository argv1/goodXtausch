import pandas as pd

def goodreads(goodreads_shelf_export_f):
    '''
        get all books from your shelf (need to be downloaded manually upfront)
        in the future missing ISBN should be added, also soft and hardcover version of the same book
    '''

    output = pd.read_csv(goodreads_shelf_export_f)   

    return output