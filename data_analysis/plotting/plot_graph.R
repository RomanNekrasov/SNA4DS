fp = file.path("data_preparation/prepared_data/network.graphml")
main_object <- igraph::read_graph(
  fp,
#   '/Users/huubvandevoort/Desktop/SNA4DS/6. Project/SNA4DS/data_preparation/prepared_data/network.graphml',
  format = "graphml"
)

graph <- main_object

# filter on edges that have edge weight > 1
to_delete <- as.vector(igraph::E(graph)[igraph::E(graph)$edge_weight <= 1])
filtered_graph <- igraph::delete_edges(graph, to_delete)

# only taking biggest component
# components <- igraph::components(graph)
# largest_component <- which.max(components$csize)
# graph <- igraph::induced_subgraph(graph, 
#                                     vids = which(components$membership == largest_component))


igraph::V(graph)$color <- "black"
igraph::V(graph) [ sentiment == 'negative' ]$color <- "#F25F5C"
igraph::V(graph) [ sentiment == 'positive' ]$color <- "#9DBF9E"
igraph::V(graph) [ sentiment == 'neutral' ]$color <- "#FFE066"

plot(
  graph,
  vertex.label = NA,
  edge.arrow.size = .05,
  edge.arrow.color = "black",
  vertex.size = (igraph::V(graph)$total_likes + 100) / 50,
  vertex.color = igraph::V(graph)$color
)

colrs <- c("#F25F5C","#9DBF9E","#FFE066")
graphics::legend(x = 0.75, y = -.85, c("Negative","Positive","Neutral"), pch = 21,
                 col = "#777777", pt.bg = colrs, pt.cex = 1.5, cex = .8, bty = "o", ncol = 1)
