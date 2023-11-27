# PURPOSE OF SCRIPT
# This script is used to combine all of the data into a single script.

# HOW 2 USE
# Set your working directory to the folder containing the scraped data.
setwd("~/Desktop/SNA4DS/6. Project/SNA4DS/test_data/scraped-15.28 26-10-2023")

### Load data
edges <- read.csv("edge_df.csv", header=TRUE, stringsAsFactors = FALSE)
vertices <- read.csv("vertex_df_icounts.csv", header=TRUE, stringsAsFactors = FALSE)

### Removing the youtube#commentThreads only keeping the "youtube#comment"s
edges <- edges[edges$kind != 'youtube#commentThread', ]

### Renaming the columns to sender and receiver
names(edges)[names(edges)=='author_id'] <- 'sender'
names(edges)[names(edges)=='dest_id'] <- 'receiver'

###  Rearranging columns to make 'sender' and 'receiver' the first two columns
###  this is required for the igraph function to create the graph object
edges <- edges[c("sender", "receiver", setdiff(names(edges), c("sender", "receiver")))]

result <- data.frame()

### Concat
# edges$senderreceiver <- paste(edges$sender, edges$receiver)
# edges <- edges[!duplicated(edges$senderreceiver), ]  # Removing duplicates
# edges$senderreceiver <- NULL

### handling NA values
edges <- edges[edges$sender != 'nan', ]
edges <- edges[edges$sender != '', ]
edges <- edges[edges$receiver != 'nan', ]
edges <- edges[edges$receiver != '', ]

### Creating graph object
graph <- igraph::graph_from_data_frame(edges, directed = TRUE, vertices = vertices)

snafun::g_summary(snafun::remove_isolates(graph))

snafun::list_vertex_attributes(graph)
snafun::list_edge_attributes(graph)

# testing if transitivity is statistically significant
ctest <- sna::cug.test(snafun::to_network(graph), FUN = sna::gtrans,
              mode = "graph",
              cmode = "edges",
              ignore.eval = TRUE, reps = 3000, FUN.args = list(use.adjacency = FALSE))
ctest
sna::plot.cug.test(ctest) # it is!

# RQ: Is the frecency of people respond to each other predicted by their subscriber_count, view_count or video_count?
interactions_out_weight_matrix <- snafun::make_matrix_from_vertex_attribute(graph,
                                                           name = "interactions_send",
                                                           measure = "sum")
diag(interactions_out_weight_matrix) <- 0
interactions_out_weight_matrix <- interactions_out_weight_matrix / rowSums(interactions_out_weight_matrix)

interactions_in_weight_matrix <- snafun::make_matrix_from_vertex_attribute(graph,
                                                           name = "interactions_received",
                                                           measure = "sum")
diag(interactions_in_weight_matrix) <- 0
interactions_in_weight_matrix <- interactions_in_weight_matrix / rowSums(interactions_in_weight_matrix)

# extracting the required variables
all_vars <- snafun::extract_all_vertex_attributes(graph)
# remove irrelevant variables
all_vars <- subset(all_vars, select = -c(member_since, display_title,
                                         customer_url, name))

autocorr <- snafun::stat_nam(interactions_send ~ .,
                             data = all_vars,
                             W = interactions_out_weight_matrix,
                             na.action(na.omit),
                             model = "lag")

summary(autocorr) # Nope definitly not! However, the interactions received is a significant
#                   predictor for sending a comment to someone.