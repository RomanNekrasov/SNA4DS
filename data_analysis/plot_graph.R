fp = file.path("/Users/huubvandevoort/Desktop/SNA4DS/6.Project/SNA4DS/data_preparation/prepared_data/network1.graphml")
main_object <- igraph::read_graph(
  fp,
#   '/Users/huubvandevoort/Desktop/SNA4DS/6. Project/SNA4DS/data_preparation/prepared_data/network.graphml',
  format = "graphml"
)

# filter on edges that have edge weight > 1
to_delete <- as.vector(igraph::E(graph)[igraph::E(graph)$edge_weight <= 1])
filtered_graph <- igraph::delete_edges(graph, to_delete)

graph <- main_object

# only taking biggest component
# components <- igraph::components(graph)
# largest_component <- which.max(components$csize)
# graph <- igraph::induced_subgraph(graph, 
#                                     vids = which(components$membership == largest_component))

# # Generate colors based on year:
colrs <- c("red", "green", "orange", "purple")


igraph::V(graph)$color == "black"
igraph::V(graph) [ sentiment == 'negative' ]$color <- "blue"
igraph::V(graph) [ sentiment == 'positive' ]$color <- "green"
igraph::V(graph) [ sentiment == 'neutral' ]$color <- "brown"
igraph::V(graph) [ sentiment == 'no sentiment' ]$color <- "orange"

#pal <- c("red", "green", "orange", "purple")
#vertex_colors <- pal[igraph::V(graph)$sentiment]

igraph::V(graph)$stress = snafun::v_stress(graph, igraph::V(graph))
igraph::V(graph)$eccentricity <- igraph::eccentricity(graph, 
                                                      vids = igraph::V(graph),
                                                      mode = 'all')


plot(
  graph,
  vertex.label = NA,
  edge.arrow.size = .1,
  vertex.size = 3,
  vertex.color = igraph::V(graph)$color
)


graphics::legend(x = -1.5, y = -1.1, c("negative","positive", "neutral", "no sentiment"), pch = 21,
                 col = "#777777", pt.bg = colrs, pt.cex = 2, cex = .8, bty = "n", ncol = 1)
