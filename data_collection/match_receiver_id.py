def match_receiver_id(edge_df, vertex_df):
  id_to_displayname = {}
  for row in range(len(vertex_df)):
    a_row = vertex_df.iloc[row]
    id_to_displayname[a_row['author_id']] = a_row['display_title']

  displayname_to_id = {}
  for row in range(len(vertex_df)):
    a_row = vertex_df.iloc[row]
    displayname_to_id[a_row['display_title']] = a_row['author_id']

  cleaned_displaynames = set(vertex_df['display_title'])

  dirty_displaynames = set(edge_df['dest_scraped'])
  unmatched_dirty_displaynames = dirty_displaynames - cleaned_displaynames

  dirty_displaynames_mapper = {}
  for string2 in list(unmatched_dirty_displaynames):
    max_length = 0
    best_match = None
    for string1 in list(cleaned_displaynames):
      if str(string2).startswith(string1) and len(string1) > max_length:
        max_length = len(string1)
        best_match = string1
    dirty_displaynames_mapper[string2] = best_match # returns a displayname: fix that!

  def match(string):
    if not string:
      return None
    if string in displayname_to_id.keys():
      return displayname_to_id[string] # returns the id
    if string in dirty_displaynames_mapper.keys():
      if dirty_displaynames_mapper[string]:
        return displayname_to_id[dirty_displaynames_mapper[string]] # returns the id
    else:
      return None

  # filling the edge_df destId column
  edge_df['dest_id'] = edge_df['dest_scraped'].apply(lambda x: match(x))


  return edge_df, vertex_df