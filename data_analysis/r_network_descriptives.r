### Set the working directory to the folder containing your data
# setwd("C:/Users/20193694/Documents/Sem 2/Social Network Analysis/data")
setwd("/Users/huubvandevoort/Desktop/SNA4DS/6.Project/SNA4DS/test_data/scraped-15.28 26-10-2023")

### Load data 
edge_df <- read.csv("edge_df.csv")
vertex_df <- read.csv("vertex_df.csv")

### Replacing empty strings with NA
edge_df$dest_id <- ifelse(edge_df$dest_id == "", NA, edge_df$dest_id)

install.packages("dplyr")

### Adding a column that includes weight, so we can remove duplicate edges 
edge_df <- edge_df |>
  dplyr::mutate(weight = ifelse(!is.na(dest_id), 1, NA))

### Grouping by that columnn to sum the weights
edge_list <- edge_df |>
  dplyr::group_by(edge_df$author_id, edge_df$dest_id) |>
  dplyr::summarize(weight = sum(weight)) |>
  dplyr::ungroup()

edge_list <- as.data.frame(edge_list)
colnames(edge_list) <- c("sender", "receiver", "weight")

### Removing rows without receiver from the edge list:
edge_list <- edge_list[complete.cases(edge_list$receiver), ]

## Change the edge_list from df to igraph
edge_i <- snafun::to_igraph(edge_list, vertices = vertex_df)

## Get NR of isolates
info <- snafun::g_summary(edge_i)
info$number_of_isolates

# Total nr of vertices
length(vertex_df$author_id)

print(edge_i)

### Get graph density 
snafun::g_density(edge_i)

# NR ISOLATES: 1098/1422 * 100 = 77.21519%
# NR EDGES: 553
# NR Connected nodes: 324
# Density: 0.0002736727

# Remove the isolates from the igraph object in order to plot without isolates
edge_no_isolates <- snafun::remove_isolates(edge_i)
plot(edge_no_isolates, main = "YouTube Network", 
     vertex.size = 3,
     edge.arrow.size = .1,
     edge.width = 0.2,
     vertex.label = NA, 
     edge.curved = .1)

# Plot the graph with isolates 
plot(edge_i, main = "YouTube Network", 
     vertex.size = 3,
     edge.arrow.size = .1,
     edge.width = 0.2,
     vertex.label = NA, 
     edge.curved = .1)


    #### PER VIDEO

# Read data
edge_df <- read.csv("edge_df.csv")
vertex_df <- read.csv("vertex_df.csv")

# Replacing empty strings with NA
edge_df$dest_id <- ifelse(edge_df$dest_id == "", NA, edge_df$dest_id)

# Create a list to store results for each video
results_list <- list()

# Open the PDF device
pdf(file = "All_Plots.pdf")

# Iterate over unique video IDs
unique_video_ids <- unique(edge_df$video_id)
for (video_id in unique_video_ids) {

  # Subset edge_df for the current video_id
  edge_subset <- edge_df[edge_df$video_id == video_id, ]

  # Adding a column that includes weight
  edge_subset <- edge_subset %>%
    mutate(weight = ifelse(!is.na(dest_id), 1, NA))

  # Create edge_list for the current video_id
  edge_list <- edge_subset %>%
    select(sender = author_id, receiver = dest_id, weight) %>%
    filter(!is.na(receiver)) %>%
    distinct() %>%
    ungroup()

  # Remove rows without receiver from the edge list
  edge_list <- edge_list[complete.cases(edge_list$receiver), ]

  # Convert edge_list to igraph
  edge_i <- to_igraph(edge_list, vertices = vertex_df)

  # Get network statistics
  info <- g_summary(edge_i)

  # Get NR of isolates
  num_isolates <- length(setdiff(edge_list$sender, edge_list$receiver))

  # Number of vertices
  num_vertices <- length(unique(c(edge_list$sender, edge_list$receiver)))
  num_commenting_vertices <- length(unique(edge_list$sender))

  # Get graph density
  density <- g_density(edge_i)

  # Print statistics for the current video_id
  cat("Video ID:", video_id, "\n")
  cat("Number of Isolates:", num_isolates, "\n")
  cat("Total Number of Vertices (including isolates):", num_vertices, "\n")
  cat("Number of Edges:", info$number_of_edges, "\n")
  cat("Number of Connected Nodes (excluding isolates):", num_commenting_vertices - num_isolates, "\n")
  cat("Density:", density, "\n\n")

  # Store results in the list
  results_list[[as.character(video_id)]] <- list(
    num_isolates = num_isolates,
    num_vertices = num_vertices,
    num_edges = info$number_of_edges,
    num_connected_nodes = num_commenting_vertices - num_isolates,
    density = density,
    edge_i = edge_i
  )

  # Plot the graph without isolates
  edge_no_isolates <- remove_isolates(edge_i)
  plot(
    edge_no_isolates,
    main = paste("YouTube Network - Video ID:", video_id, "(No Isolates)"),
    vertex.size = 3,
    edge.arrow.size = 0.1,
    edge.width = 0.2,
    vertex.label = NA,
    edge.curved = 0.1
  )

  # Plot the graph with isolates
  plot(
    edge_i,
    main = paste("YouTube Network - Video ID:", video_id, "(With Isolates)"),
    vertex.size = 3,
    edge.arrow.size = 0.1,
    edge.width = 0.2,
    vertex.label = NA,
    edge.curved = 0.1
  )
}

# Close the PDF device
dev.off()

# Combine the results into a data frame
results_df <- do.call(rbind, results_list)

# Print the results data frame
print(results_df[ ,0:5])
