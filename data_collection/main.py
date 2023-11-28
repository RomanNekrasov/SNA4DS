import datetime
import sys

import pandas as pd
import os
import logging
import argparse

from config import constants as c
from collect_edge_data import collect_comments_of_video
from collect_vertex_data import collect_vertex_data
from match_receiver_id import match_receiver_id
from helpers import chunks
from count_vertex_interactions import count_interactions


def main(video_id: str | list):
    vertex_df = pd.DataFrame(
        columns=['author_id', 'display_title', 'customer_url', 'member_since', 'subscriber_count', 'view_count',
                 'video_count']
    )
    edge_df = pd.DataFrame(
        columns=['thread_id', 'video_id', 'comment_id', 'time', 'kind', 'author_id', 'dest_scraped', 'likes',
                 'num_replies', 'text']
    )

    if isinstance(video_id, str):  # When a single video ID is used to call the function, it will be converted to list
        video_id = list(video_id)

    for v_id in video_id:
        logging.info(f"...Collecting data from {v_id}...")
        edge_df = collect_comments_of_video(edge_df=edge_df, video_id=v_id)

    # getting unique author ids from the edge df
    all_author_ids = list(edge_df['author_id'].unique())
    print(f'Number of unique IDs: {len(all_author_ids)}')
    all_author_ids_comma_sep = chunks(all_author_ids, 50)

    vertex_df = collect_vertex_data(frame=vertex_df, author_ids=all_author_ids_comma_sep)

    # matching the scraped handles of the receivers with the actual author ids
    edge_df, vertex_df = match_receiver_id(edge_df=edge_df, vertex_df=vertex_df)

    vertex_df = count_interactions(edge_df, vertex_df)

    new_dir = f'test_data/scraped-{datetime.datetime.now().strftime("%H.%M %d-%m-%Y")}'
    os.mkdir(new_dir)
    vertex_df.to_csv(f'{new_dir}/vertex_df.csv', index=False)
    edge_df.to_csv(f'{new_dir}/edge_df.csv', index=False)
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
    main(video_id=parse_command_line_arguments().get('video_id'))
