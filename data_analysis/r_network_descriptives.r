### Set the working directory to the folder containing your data
setwd("/Users/huubvandevoort/Desktop/SNA4DS/SNA4DS/test_data/scraped-15.28 26-10-2023")

### Load data 
edge_df <- read.csv("edge_df.csv")
head(edge_df)

vertex_df <- read.csv("vertex_df.csv")
head(vertex_df)

### Replacing empty strings with NA
edge_df$dest_id <- ifelse(edge_df$dest_id == "", NA, edge_df$dest_id)

install.packages("dplyr")

### Adding a column that includes weight, so we can remove duplicate edges 
edge_df <- edge_df %>%
  dplyr::mutate(weight = ifelse(!is.na(dest_id), 1, NA))

edge_list <- edge_df %>% 
  dplyr::group_by(edge_df$author_id, edge_df$dest_id) %>%
  dplyr::summarize(weight = sum(weight)) %>%
  dplyr::ungroup()

edge_list <- as.data.frame(edge_list)
colnames(edge_list) <- c("sender", "receiver", "weight")

### Removing rows without receiver from the edge list:
edge_list <- edge_list[complete.cases(edge_list$receiver), ]

## Change the edge_list from df to igraph
edge_i <- snafun::to_igraph(edge_list, vertices = vertex_df)
# ?snafun::to_igraph

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
