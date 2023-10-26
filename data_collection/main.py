import datetime
import sys

import pandas as pd
import os
import logging
import argparse

from config import constants as c
from collect_edge_data import collect_comments
from collect_vertex_data import collect_vertex_data
from match_receiver_id import match_receiver_id
from helpers import chunks


# TODO: add docstrings
# TODO: check if a the destination of a comment on a comment is is properly registrated
# TODO: Check if the regex expression in collect_edge_data.py is correct


def main(video_id: str | list, edge_df=pd.DataFrame(columns=['comment_id', 'threath_id', 'time', 'kind', 'author_id',
                                                'dest_scraped', 'likes', 'num_replies', 'text', 'video_id']),
         vertex_df=pd.DataFrame(columns=['author_id', 'display_title', 'customer_url', 'member_since',
                                         'subscriber_count', 'view_count', 'video_count'])):

    if isinstance(video_id, str):
        video_id = list(video_id)

    for v_id in video_id:
        # function that fills the edge dataframe
        logging.info(f"...Collecting data from {v_id}...")
        edge_df = collect_comments(edge_df=edge_df, videoId=v_id)

    # getting unique authorIds from the edge df
    all_authorIds = list(edge_df['author_id'].unique())
    print(f'Number of unique IDs: {len(all_authorIds)}')
    all_authorIds_comma_sep = chunks(all_authorIds, 50)

    vertex_df = collect_vertex_data(frame=vertex_df, ids=all_authorIds_comma_sep)

    # matching the scraped handles of the receivers with the actual AuthorIds
    edge_df, vertex_df = match_receiver_id(edge_df=edge_df, vertex_df=vertex_df)

    newdir = f'test_data/scraped-{datetime.datetime.now().strftime("%H.%M %d-%m-%Y")}'
    os.mkdir(newdir)
    vertex_df.to_csv(f'{newdir}/vertex_df.csv', index=False)
    edge_df.to_csv(f'{newdir}/edge_df.csv', index=False)
    logging.info("...executed...")


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_id', type=str, nargs='+')
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    # main function call
    # The video_id is the last part of the youtube url
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    main(video_id=parse_command_line_arguments().get('video_id', 'nan'))
