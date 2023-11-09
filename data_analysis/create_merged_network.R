# PURPOSE OF SCRIPT
# This script is used to combine all of the data into a single script.

# HOW 2 USE
# Set your working directory to the folder containing the scraped data.
setwd("~/Desktop/SNA4DS/6. Project/SNA4DS/test_data/scraped-15.28 26-10-2023")

### Load data
edges <- read.csv("edge_df.csv", header=TRUE, stringsAsFactors = FALSE)

### Removing the youtube#commentThreads only keeping the "youtube#comment"s
edges <- edges[edges$kind != 'youtube#commentThread', ]

### Renaming the columns to sender and receiver
names(edges)[names(edges)=='author_id'] <- 'sender'
names(edges)[names(edges)=='dest_id'] <- 'receiver'

### Only keeping the relevant columns
edges <- edges[, c('sender', 'receiver')]

result <- data.frame()

### Concat
edges$senderreceiver <- paste(edges$sender, edges$receiver)
edges <- edges[!duplicated(edges$senderreceiver), ]  # Removing duplicates
edges$senderreceiver <- NULL

edges$receiver <- ifelse(edges$receiver == "", NA, edges$receiver)
edges$receiver <- ifelse(edges$receiver == "nan", NA, edges$receiver)

### Creating graph object
suppressWarnings({
graph <- igraph::graph_from_data_frame(edges, directed = TRUE) |>
  snafun::remove_loops() |>
  snafun::remove_vertices(vertices = "NA")
})

plot(
    snafun::remove_isolates(graph),
    vertex.label=NA,
    vertex.size = 2,
    vertex.color = "red",
    edge.arrow.size = .5,
    edge.color = "grey",
    main = "Plot of merged graph"
  )

### Getting descriptives
result <- data.frame()
sum <- snafun::g_summary(graph)
r <- list(
  number_of_vertices = sum$number_of_vertices,
  number_of_edges = sum$number_of_edges,
  number_of_isolates = sum$number_of_isolates,
  number_of_connected_nodes = sum$number_of_vertices - sum$number_of_isolates,
  density = sum$density,
  density_without_isolates = snafun::g_summary(snafun::remove_isolates(graph))$density,
  triad_030t = snafun::count_triads(graph)$"030T"
)
result <- rbind(result, r)

write.csv(result, "merged_network_descriptives.csv", row.names = FALSE)
