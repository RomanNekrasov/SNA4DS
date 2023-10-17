from collect_edge_data import *
from collect_vertex_data import *
import pandas as pd

def main(videoId, edge_df=pd.DataFrame(columns=['comment_id', 'threath_id', 'time', 'kind', 'author',
                                                'dest', 'likes','num_replies','text', 'video_id']),
                  vertex_df=pd.DataFrame(columns=['author_id', 'display_title', 'customer_url', 'member_since',
                                                  'subscriber_count', 'view_count', 'video_count'])):

  # function that collects the edge dataframe
  edge_df = collect_comments(edge_df=edge_df, videoId=videoId)

  def chunks(lst, n):
    """Helper function that splits the unqiue authorIds into chunks of 50
       because the youtube api only allows 50 ids per request

    Keyword arguments:
    lst: list -- list of authorids
    Return: a list of strings of comma separated authorIds
    """

    result = []
    for i in range(0, len(lst), n):
        result.append(','.join(lst[i:i + n]))
    return result

  # getting unique authorIds from the edge df
  all_authorIds = list(edge_df['author'].unique())
  print(f'Number of unique IDs: {len(all_authorIds)}')
  all_authorIds_comma_sep = chunks(all_authorIds, 50)

  vertex_df = collect_vertex_data(frame=vertex_df, ids=all_authorIds_comma_sep)

  vertex_df.to_csv(f'vertex_df-{videoId}.csv')
  edge_df.to_csv(f'edge_df-{videoId}.csv')
  print('executed')

# main function call
# The videoId is the last part of the youtube url
main(videoId="5ChkQKUzDCs")