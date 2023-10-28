import pandas as pd


def match_receiver_id(edge_df, vertex_df):
    """ Uses the set of collected author ids from the vertex_df to request the username belonging to each author id
     using the YouTube api. Then, it fills the dest_id column in the edge_df with the user_id by matching
     the username in the scraped comment text with the actual username retrieved from the YouTube API. This way, the
     author ids of the comments that include handles ('@') are matched with destination ids.
    Keyword arguments:
      edge_df: pd.Dataframe with collected edges
      vertex_df: pd.Dataframe with all different vertices involved
    """

    # Creating a mapper that maps the display_title to the author id
    display_name_to_id = {}
    for row in range(len(vertex_df)):
        a_row = vertex_df.iloc[row]
        display_name_to_id[a_row['display_title']] = a_row['author_id']

    clean_display_names = set(vertex_df['display_title'])

    dirty_display_names = set(edge_df['dest_scraped'])  # The patterns matched with regex
    #  Removing the names that can already be matched to one of the clean display names
    unmatched_dirty_display_names = dirty_display_names - clean_display_names

    dirty_display_names_mapper = {}  # Used to map a dirty display names with their best match
    for string2 in list(unmatched_dirty_display_names):
        max_length = 0
        best_match = None  # Used to select the longest matching string
        for string1 in list(clean_display_names):
            if str(string2).startswith(string1) and len(string1) > max_length:
                max_length = len(string1)
                best_match = string1
        dirty_display_names_mapper[string2] = best_match  # returns a display name: fix that!

    def match(string):
        if not string:
            return None
        if string in display_name_to_id.keys():
            return display_name_to_id[string]  # returns the id
        if string in dirty_display_names_mapper.keys():
            if dirty_display_names_mapper[string]:
                return display_name_to_id[dirty_display_names_mapper[string]]  # returns the id
        else:
            return 'NF'  # Returns Not Found when it was not able to match the handle with an existing id

    # filling the edge_df destId column
    edge_df['dest_id'] = edge_df['dest_scraped'].apply(lambda x: match(x))

    return edge_df, vertex_df
