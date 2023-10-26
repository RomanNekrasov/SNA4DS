from config import constants as c
import googleapiclient.discovery
import pandas as pd


def enable_api():
    youtube = googleapiclient.discovery.build(
        c.API_SERVICE_NAME, c.API_VERSION, developerKey=c.YOUTUBE_API_KEY, cache_discovery=False)
    return youtube


def add_to_frame(frame, an_item):
    """ Takes the dataframe and appends an item to the rows
    Keyword arguments:
    edge_df -- the dataframe
    an_item -- the item to be appended

    Return:
    returns the dataframe with the appended item
    """

    frame.loc[len(frame) + 1] = an_item
    return frame


def chunks(lst, n):
    """Helper function that splits the unqiue authorIds into chunks of 50
   because the youtube api only allows 50 ids per request

    Keyword arguments:
    lst: list -- list of authorids
    Return: a list of strings of comma separated authorIds
    """

    result = []
    for i in range(0, len(lst), n):
        result.append(','.join(lst[i:i + n]))
    return result
