import pandas as pd
import argparse


def count_interactions(edge_df, vertex_df):
    """
    Function that will count the outward and inward interactions of a vertex and then adds two
    new columns to the vertex dataframe.
    """

    def _find_interaction_count(reference, val):
        if val in set(reference.index):
            return reference.loc[val]
        else:
            return 0

    senders = edge_df['author_id'].value_counts()
    receivers = edge_df['dest_id'].value_counts()

    vertex_df['interactions_send'] = vertex_df['author_id'].apply(lambda x: _find_interaction_count(senders, x))
    vertex_df['interactions_received'] = vertex_df['author_id'].apply(lambda x: _find_interaction_count(receivers, x))

    return vertex_df


# For testing
def parse_command_line_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--edge_df_path', type=str)
    parser.add_argument('--vertex_df_path', type=str)
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    # main function call
    args = parse_command_line_arguments()
    edge_df_path = args.get('edge_df_path')
    vertex_df_path = args.get('vertex_df_path')
    edge_df = pd.read_csv(edge_df_path)
    vertex_df = pd.read_csv(vertex_df_path)
    vertex_df = count_interactions(edge_df=edge_df, vertex_df=vertex_df)
    vertex_df.to_csv(
        '/Users/huubvandevoort/Desktop/SNA4DS/6. Project/SNA4DS/test_data/scraped-15.28 26-10-2023/vertex_df_icounts.csv',
        index=False
    )

