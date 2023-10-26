import datetime
import pandas as pd
import os

from config import constants as c
from collect_edge_data import collect_comments
from collect_vertex_data import collect_vertex_data
from match_receiver_id import match_receiver_id
from helpers import chunks


# TODO: add docstrings
# TODO: check if a the destination of a comment on a comment is is properly registrated
# TODO: Check if the regex expression in collect_edge_data.py is correct


def main(videoId, edge_df=pd.DataFrame(columns=['comment_id', 'threath_id', 'time', 'kind', 'author_id',
                                                'dest_scraped', 'likes', 'num_replies', 'text', 'video_id']),
         vertex_df=pd.DataFrame(columns=['author_id', 'display_title', 'customer_url', 'member_since',
                                         'subscriber_count', 'view_count', 'video_count'])):
    # function that fills the edge dataframe
    edge_df = collect_comments(edge_df=edge_df, videoId=videoId)


    # getting unique authorIds from the edge df
    all_authorIds = list(edge_df['author_id'].unique())
    print(f'Number of unique IDs: {len(all_authorIds)}')
    all_authorIds_comma_sep = chunks(all_authorIds, 50)

    vertex_df = collect_vertex_data(frame=vertex_df, ids=all_authorIds_comma_sep)

    # matching the scraped handles of the receivers with the actual AuthorIds
    edge_df, vertex_df = match_receiver_id(edge_df=edge_df, vertex_df=vertex_df)

    newdir = f'scraped-{videoId}-{datetime.datetime.now().strftime("%H.%M %d-%m-%Y")}'
    os.mkdir(newdir)
    vertex_df.to_csv(f'{newdir}/vertex_df-{videoId}.csv', index=False)
    edge_df.to_csv(f'{newdir}/edge_df-{videoId}.csv', index=False)
    print('executed')


# main function call
# The videoId is the last part of the youtube url
main(videoId="1pWjP9QNLcg")
