import re
import pandas as pd
import numpy as np
import logging
import sys
import os
import googleapiclient.discovery
import personalConstants as pc
import constants as c

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1" # From the documentation https://developers.google.com/youtube/v3/docs/

logging.basicConfig(stream=sys.stdout, level=logging.INFO) # to see what the code is doing when running

def add_to_frame(frame, an_item):
  """ Takes the dataframe and appends an item to the rows

  Keyword arguments:
  edge_df -- the dataframe
  an_item -- the item to be appended

  Return:
  returns the dataframe with the appended item
  """

  frame.loc[len(frame)+1] = an_item
  return frame

def enable_api():
  youtube = googleapiclient.discovery.build(
      c.API_SERVICE_NAME, c.API_VERSION, developerKey=c.YOUTUBEAPIKEY, cache_discovery=False)
  return youtube

def get_comments_from_threath(threath_id):
  """This function gets the replies to a top level comment

  Keyword arguments:
  threath_id -- str: that is the id of the top level comment
  Return: all the replies in a list
  """
  youtube = enable_api()

  # sending first request
  request_comments = youtube.comments().list(
      part = "snippet",
      parentId = threath_id,
      maxResults = 100
  )

  data = request_comments.execute()
  replies = data['items'] # initial list of replies

  # getting the pagetoken if there is one
  if 'nextPageToken' in set(data.keys()):
    pageToken = data['nextPageToken']
  else:
    pageToken = None

  while pageToken: # if there is a next page, getting those replies as well
    request_comments = youtube.comments().list(
        part = "snippet",
        parentId = threath_id,
        pageToken = pageToken,
        maxResults = 100
    )
    data = request_comments.execute()

    # now merge the two lists
    replies = replies + data['items']

    # getting the pagetoken if there is one
    if 'nextPageToken' in set(data.keys()):
      pageToken = data['nextPageToken']
    else:
      pageToken = None
  logging.info('Replies collected')
  return replies

def send_request(videoId, pageToken=None):
  """Base function for communicating with the youtube API
     it uses the YouTube commentThreads to get the top level comments

  Keyword arguments:
  pageToken -- the token received from the previous request
  Return: the response from the API in JSON format
  """
  youtube = enable_api()
  if pageToken == None:
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoId,
    )
  else:
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId=videoId,
        pageToken=pageToken
    )
  data = request.execute()
  logging.info('Request sent')
  return data

def parse_item_top_comment(an_item):
  """Parses the top comment since this is slightly different than a reply to a top comment

  Keyword arguments:
  an_item -- This is one of the items from the list of items that is returned from the API call
  Return: returns a tuple with the parsed data see below for the order
  """
  video_id = an_item['snippet']['videoId']
  threath_id = an_item['id']
  comment_id = threath_id # top comment has the same id as the thread
  kind = an_item['kind']  # always 'youtube#commentThread'
  time = an_item['snippet']['topLevelComment']['snippet']['publishedAt']
  author = an_item['snippet']['topLevelComment']['snippet']['authorChannelId']['value']
  num_replies = an_item['snippet']['totalReplyCount']
  likes = an_item['snippet']['topLevelComment']['snippet']['likeCount']
  text = an_item['snippet']['topLevelComment']['snippet']['textOriginal']
  dest = np.nan # top comment has no destination
  return comment_id, threath_id, time, kind, author, dest, likes, num_replies, text, video_id

def parse_reply(a_reply, video_id):
  video_id = video_id
  threath_id = a_reply['snippet']['parentId']
  comment_id = a_reply['id']
  kind = a_reply['kind'] # always 'youtube#comment'
  time = a_reply['snippet']['publishedAt']
  author = a_reply['snippet']['authorChannelId']['value']
  likes = a_reply['snippet']['likeCount']
  num_replies = np.nan # for youtube#comment there are no replies
  text = a_reply['snippet']['textOriginal']

  if '@' in text:
    dest = re.findall(r"@(\S+\s*\S*)", text)[0]
  else:
    dest = ''

  return comment_id, threath_id, time, kind, author, dest, likes, num_replies, text, video_id

def collect_comments(videoId, edge_df):
  """Function that combines the other functions to collect the comments

  Keyword arguments:
  edge_df -- a pandas dataframe that will be filled with the comments
  Return: the dataframe with the comments
  """

  # sending initial request
  response = send_request(videoId=videoId)
  while len(edge_df) < 300000:
    # Parsing
    items = response['items']
    for x in items: # x is a top level comment item
      # top level comment
      item = parse_item_top_comment(x)
      video_id = item[9]
      edge_df = add_to_frame(edge_df, item)

      if x["snippet"]["totalReplyCount"] > 0:
        threath_id = item[1]
        replies = get_comments_from_threath(threath_id=threath_id)
        for reply in replies:
          reply = parse_reply(reply, video_id) # had to give it video id because this is not in the reply repsonse
          edge_df = add_to_frame(edge_df, reply)

     # sending next request
    if 'nextPageToken' in set(response.keys()):
      response = send_request(videoId=videoId, pageToken=response['nextPageToken'])
      logging.info('Requesting Next page')
    else:
      logging.info('Returned because: No more pages')
      return edge_df
  logging.info('Returned because: The other option')
  return edge_df