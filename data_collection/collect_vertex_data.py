from data_collection.helpers import enable_api, add_to_frame
import pandas as pd
import logging
import sys
import argparse


def request_author_information(author_ids: str):
    """ Function that returns the information about a channel that
    """
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)  # to see what the code is doing when running
    youtube = enable_api()
    request = youtube.channels().list(
        part="snippet,statistics",
        id=author_ids,
        maxResults=50
    )
    response = request.execute()
    logging.info(f"Requested channel information")
    return response


def parse_response(response, frame):
    """ Function that parses the required information from a response and adds it to the resulting dataframe
    Keywords:
        response - the response resulting from the request_author_information function
        frame - the resulting dataframe
    Return:
        the filled dataframe
    """
    logging.info(f"Number of responses: {len(response.get('items'))}")

    # parsing response
    for i in response['items']:
        author_id = i['id']
        author_title = i['snippet']['title']
        custom_url = i['snippet']['customUrl']
        member_since = i['snippet']['publishedAt']
        subscriber_count = i['statistics']['subscriberCount']
        view_count = i['statistics']['viewCount']
        video_count = i['statistics']['videoCount']
        newline = [author_id, author_title, custom_url, member_since, subscriber_count, view_count, video_count]
        # adding to frame
        frame = add_to_frame(frame, newline)
    return frame


def collect_vertex_data(frame, author_ids):
    """ Integration function for requesting channel information and parsing the response
  Keyword arguments:
      frame -- the pd.Dataframe that will be returned it should have 7 columns be in the format: 'author_id',
                'display_title', 'customer_url', 'member_since', 'subscriber_count', 'view_count', 'video_count'
      author_ids -- the set of different author_ids that are collected in the edge pd.Dataframe
  Return:
      the pd.Dataframe with the new information added
  """
    for idset in author_ids:
        response = request_author_information(author_ids=idset)
        print(response)
        frame = parse_response(response, frame)
    return frame


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', type=str)
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    # main function call
    # The video_id is the last part of the youtube url
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    test_frame = pd.DataFrame(
        columns=['author_id', 'display_title', 'customer_url', 'member_since', 'subscriber_count', 'view_count',
                 'video_count']
    )

    collect_vertex_data(author_ids=[parse_command_line_arguments().get('ids')],
                        frame=test_frame).to_csv('test_data/test123.csv', index=False)
