setwd("/Users/huubvandevoort/Desktop/SNA4DS/SNA4DS/test_data/scraped-15.28 26-10-2023")

### Load data
edges <- read.csv("edge_df.csv", header=TRUE, stringsAsFactors = FALSE)
vertex_df <- read.csv("vertex_df.csv", header=TRUE, stringsAsFactors = FALSE)

### Renaming the columns to sender and receiver
names(edges)[names(edges)=='author_id'] <- 'sender'
names(edges)[names(edges)=='dest_id'] <- 'receiver'

edges <- edges[, c('sender', 'receiver', 'video_id')]

result <- data.frame(
  video_id = str(0),
  number_of_vertices = numeric(0),
  number_of_edges = numeric(0),
  number_of_isolates = numeric(0),
  number_of_connected_nodes = numeric(0),
  density = numeric(0),
  density_without_isolates = numeric(0)
)

for (vid in unique(edges$video_id)) {
  current_edges <- edges[edges$video_id == vid,]

  ### Concat
  current_edges$senderreceiver <- paste(current_edges$sender, current_edges$receiver)
  current_edges <- current_edges[!duplicated(current_edges$senderreceiver), ]  # Removing duplicates
  current_edges$senderreceiver <- NULL

  current_edges$receiver <- ifelse(current_edges$receiver == "", NA, current_edges$receiver)
  current_edges$receiver <- ifelse(current_edges$receiver == "nan", NA, current_edges$receiver)

  ### Creating graph object
  suppressWarnings({
  graph <- igraph::graph_from_data_frame(current_edges, directed = TRUE) |>
    snafun::remove_loops() |>
    snafun::remove_vertices(vertices = "NA")
  })
  sum <- snafun::g_summary(graph)

  r <- list(
    video_id = vid,
    number_of_vertices = sum$number_of_vertices,
    number_of_edges = sum$number_of_edges,
    number_of_isolates = sum$number_of_isolates,
    number_of_connected_nodes = sum$number_of_vertices - sum$number_of_isolates,
    density = sum$density,
    density_without_isolates = snafun::g_summary(snafun::remove_isolates(graph))$density
  )
  result <- rbind(result, r)
}
print(result)
write.csv(result, 'output.csv')
# plot(snafun::remove_isolates(graph), vertex.label=NA, vertex.size = 3, edge.arrow.size = .2, edge.color = "blue")
