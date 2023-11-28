import re
import numpy as np
import pandas as pd
import logging
import sys
import os
import googleapiclient.discovery
from helpers import enable_api, add_to_frame

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # From the documentation https://developers.google.com/youtube/v3/docs/
logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # to see what the code is doing when running


def get_next_page_token(response_data):
    # getting the nextPageToken if there is one
    if 'nextPageToken' in set(response_data.keys()):
        page_token = response_data['nextPageToken']
    else:
        page_token = None
    return page_token


def request_replies_on_main_thread(thread_id):
    """
    This function requests the replies to a main thread

    Keyword arguments:
        thread_id -- str: that is the id of the main thread
    Return: all the replies in a list
    """

    youtube = enable_api()

    # sending first request
    request_comments = youtube.comments().list(
        part="snippet",
        parentId=thread_id,
        maxResults=100
    )

    data = request_comments.execute()  # executes the request
    replies = data['items']  # initial list of replies

    page_token = get_next_page_token(response_data=data)  # getting the nextPageToken if there is no, then page_token
    # is None

    while page_token:  # if there is a next page, getting those replies as well
        request_comments = youtube.comments().list(
            part="snippet",
            parentId=thread_id,
            pageToken=page_token,
            maxResults=100
        )
        data = request_comments.execute()

        # now merge the two lists
        replies = replies + data['items']

        page_token = get_next_page_token(response_data=data)  # getting the nextPageToken if there is one

    logging.info('...Replies collected...')
    return replies


def request_main_comment_thread(video_id, page_token=None):
    """Base function for communicating with the youtube API
     it uses the YouTube commentThreads to get the top level comments

  Keyword arguments:
  page_token -- the token received from the previous request
  Return: the response from the API in JSON format
  """
    youtube = enable_api()
    if page_token:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            pageToken=page_token
        )
    else:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
        )
    response = request.execute()
    logging.info('Request sent')
    return response


def parse_main_thread_response(api_return_item):
    """Parses the top comment since this is slightly different than a reply to a top comment

  Keyword arguments:
  api_return_item -- This is one of the items from the list of items that is returned from the API call
  Return: returns a tuple with the parsed data see below for the order
  """

    thread_id = api_return_item['id']
    video_id = api_return_item['snippet']['videoId']
    comment_id = thread_id  # top comment has the same id as the thread
    time = api_return_item['snippet']['topLevelComment']['snippet']['publishedAt']
    kind = api_return_item['kind']  # always 'youtube#commentThread'
    author = api_return_item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
    dest = np.nan  # top comment has no destination
    likes = api_return_item['snippet']['topLevelComment']['snippet']['likeCount']
    num_replies = api_return_item['snippet']['totalReplyCount']
    text = api_return_item['snippet']['topLevelComment']['snippet']['textOriginal']

    return thread_id, video_id, comment_id, time, kind, author, dest, likes, num_replies, text


def parse_reply_on_main_thread(reply, video_id):
    thread_id = reply['snippet']['parentId']
    video_id = video_id
    comment_id = reply['id']
    time = reply['snippet']['publishedAt']
    kind = reply['kind']  # always 'youtube#comment'
    author = reply['snippet']['authorChannelId']['value']
    likes = reply['snippet']['likeCount']
    num_replies = np.nan  # for youtube#comment there are no replies
    text = reply['snippet']['textOriginal']
    if '@' in text:
        dest = re.findall(r"@(\S+\s*\S*\s*\S*)", text)[0]
    else:
        dest = ''

    return thread_id, video_id, comment_id, time, kind, author, dest, likes, num_replies, text


def collect_comments_of_video(video_id, edge_df):
    """Integration Function that combines the other functions to collect the comments

  Keyword arguments:
  edge_df -- a pd.Dataframe that will be filled with the comments
  video_id -- the video id of the video of which the comments have to be collected
  Return: the dataframe with the comments
  """

    # sending initial request
    response = request_main_comment_thread(video_id=video_id)
    while True:
        # Parsing
        items = response['items']
        for x in items:  # x is a top level comment item
            # top level comment
            item = parse_main_thread_response(x)
            # video_id = item[9]
            edge_df = add_to_frame(edge_df, item)

            if x["snippet"]["totalReplyCount"] > 0:  # This gets executed when people replied on the main thread
                thread_id = item[1]
                replies = request_replies_on_main_thread(thread_id=thread_id)
                for reply in replies:
                    # had to give parse_reply video id as parameter because this is not in the reply response
                    reply = parse_reply_on_main_thread(reply, video_id)
                    edge_df = add_to_frame(edge_df, reply)

        if 'nextPageToken' in set(response.keys()):  # sending next request
            response = request_main_comment_thread(video_id=video_id, page_token=response['nextPageToken'])
            logging.info('...Requesting Next page...')
        else:
            logging.info('Done: No more pages')
            return edge_df
