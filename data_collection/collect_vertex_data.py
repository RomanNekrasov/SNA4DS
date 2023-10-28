from helpers import enable_api, add_to_frame
import pandas as pd
import logging
import sys


def request_author_information(author_ids: str):
    """ Function that returns the information about a channel that
    """
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # to see what the code is doing when running
    youtube = enable_api()
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=author_ids,
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
      frame -- the pd.Dataframe that will be returned it should have 7 columns be in the format: 'author_id',
                'display_title', 'customer_url', 'member_since', 'subscriber_count', 'view_count', 'video_count'
      author_ids -- the set of different author_ids that are collected in the edge pd.Dataframe
  Return:
      the pd.Dataframe with the new information added
  """
    for idset in ids:
        response = request_channel_information(ids=idset)
        frame = parse_responses(response, frame)
    return frame
