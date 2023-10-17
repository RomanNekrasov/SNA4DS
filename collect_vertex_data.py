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
  for idset in ids:
    response = request_channel_information(ids=idset)
    frame = parse_responses(response, frame)
  return frame

# 1. send initial request
# 2. Parse the list of items in the response
#     if there is a nextpagekey:
# 3. Get the nextpagekey if there is one
# 4. send new request
# 5. do the same
# 6. return the final dataframe

# getting the list of authorIds from the edge df
def chunks(lst, n):
    """function that splits the unqiue authorIds into chunks of 50 because the youtube api only allows 50 ids per request

    Keyword arguments:
    lst: list -- list of authorids
    Return: a list of strings of comma separated authorIds
    """

    result = []
    for i in range(0, len(lst), n):
        result.append(','.join(lst[i:i + n]))
    return result