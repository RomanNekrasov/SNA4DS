import re
import pandas as pd
import numpy as np
import logging
import sys
import googleapiclient.discovery
import json
import personalConstants as pc
import constants as c

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

def add_to_frame(edge_df, an_item):
  """ Takes the dataframe and appends an item to the rows

  Keyword arguments:
  edge_df -- the dataframe
  an_item -- the item to be appended

  Return:
  returns the dataframe with the appended item
  """

  edge_df.loc[len(edge_df)+1] = an_item
  return edge_df

def send_request(pageToken=None):
  """Base function for communicating with the youtube API

  Keyword arguments:
  pageToken -- the token received from the previous request
  Return: the response from the API in JSON format
  """

  API_KEY=pc.YOUTUBEAPIKEY
  API_SERVICE_NAME = c.API_SERVICE_NAME
  API_VERSION = c.API_VERSION

  youtube = googleapiclient.discovery.build(
      API_SERVICE_NAME, API_VERSION, developerKey=API_KEY, cache_discovery=False)

  if pageToken == None:
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId="1pWjP9QNLcg",
    )
  else:
    request = youtube.commentThreads().list(
        part="snippet,replies",
        videoId="1pWjP9QNLcg",
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
  likes = an_item['snippet']['topLevelComment']['snippet']['likeCount']
  text = an_item['snippet']['topLevelComment']['snippet']['textOriginal']
  dest = np.nan # top comment has no destination
  return comment_id, threath_id, time, kind, author, dest, likes, text, video_id

def parse_reply(a_reply):
  video_id = a_reply['snippet']['videoId']
  threath_id = a_reply['snippet']['parentId']
  comment_id = a_reply['id']
  kind = a_reply['kind'] # always 'youtube#comment'
  time = a_reply['snippet']['publishedAt']
  author = a_reply['snippet']['authorChannelId']['value']
  likes = a_reply['snippet']['likeCount']
  text = a_reply['snippet']['textOriginal']

  if '@' in text:
    dest = re.findall(r'@(\w+)', text)[0]
  else:
    dest = ''

  return comment_id, threath_id, time, kind, author, dest, likes, text, video_id

def collect_comments(edge_df):
  if len(edge_df) > 50000:
    logging.info('Dataframe is full')
    return edge_df

  # sending initial request
  response = send_request()
  while len(edge_df) < 300000:
    # Parsing
    items = response['items']
    for x in items:
      # top level comment
      item = parse_item_top_comment(x)
      edge_df = add_to_frame(edge_df, item)

      # replies to top level comment
      if 'replies' in set(x.keys()):
        replies = x['replies']['comments']
        for reply in replies:
          reply = parse_reply(reply)
          edge_df = add_to_frame(edge_df, reply)

     # sending next request
    if 'nextPageToken' in set(response.keys()):
      response = send_request(pageToken=response['nextPageToken'])
      logging.info('Next page')
    else:
      logging.info('No more pages')
      return edge_df
  logging.info('The other option')
  return edge_df

def main(edge_df):
  edge_df = collect_comments(edge_df=edge_df)
  edge_df.to_csv('edge_df.csv')
  print('executed')

# defining what result df should look like
edge_df = pd.DataFrame(columns=['comment_id', 'threath_id', 'time', 'kind', 'author', 'dest', 'likes', 'text', 'video_id'])

# main function call
main(edge_df=edge_df)