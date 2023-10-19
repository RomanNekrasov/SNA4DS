from collect_edge_data import enable_api, add_to_frame
import pandas as pd
import logging
import sys

def request_channel_information(ids):
  logging.basicConfig(stream=sys.stdout, level=logging.INFO) # to see what the code is doing when running
  youtube = enable_api()
  request = youtube.channels().list(
        part = "snippet,contentDetails,statistics",
        id=ids,
        maxResults=50
        )
  response = request.execute()
  logging.info(f"Requested channel information")
  return response


def parse_responses(response, frame):
  logging.info(f"Number of responses: {len(response['items'])}")

  # parsing response
  for i in response['items']:
    authorId = i['id']
    authorTitle = i['snippet']['title']
    customUrl = i['snippet']['customUrl']
    memberSince = i['snippet']['publishedAt']
    subscriberCount = i['statistics']['subscriberCount']
    viewCount = i['statistics']['viewCount']
    videoCount = i['statistics']['videoCount']
    newline = [authorId, authorTitle, customUrl, memberSince, subscriberCount, viewCount, videoCount]
    # adding to frame
    frame = add_to_frame(frame, newline)
  return frame

def collect_vertex_data(frame, ids):
  """ Integration function for requesting channel information and parsing the response

  Keyword arguments:
  frame -- the dataframe that will be returned it should have 7 columns be in the format:
            authorId, authorTitle, customUrl, memberSince, subscriberCount, viewCount, videoCount
  Return: the dataframe with the new information added
  """

  for idset in ids:
    response = request_channel_information(ids=idset)
    frame = parse_responses(response, frame)
  return frame

# HOW IT WORKS:
# 1. The author ids are parsed into chunks of 50 items then each chunk is sent as a request
# 2. Parse the list of items in the response
# 3. Add the parsed items to the dataframe
# 4. Repeat until all chunks have been requested
# 5. Return the dataframe