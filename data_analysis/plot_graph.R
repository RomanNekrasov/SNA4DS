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

# # Generate colors based on year:
colrs <- c("#FFE066", "#F25F5C", "#9DBF9E", "#05204A")


igraph::V(graph)$color == "black"
igraph::V(graph) [ sentiment == 'negative' ]$color <- "#9DBF9E"
igraph::V(graph) [ sentiment == 'positive' ]$color <- "#FFE066"
igraph::V(graph) [ sentiment == 'neutral' ]$color <- "#F25F5C"
igraph::V(graph) [ sentiment == 'no sentiment' ]$color <- "#05204A"

#pal <- c("red", "green", "orange", "purple")
#vertex_colors <- pal[igraph::V(graph)$sentiment]

igraph::V(graph)$stress = snafun::v_stress(graph, igraph::V(graph))
igraph::V(graph)$eccentricity <- igraph::eccentricity(graph, 
                                                      vids = igraph::V(graph),
                                                      mode = 'all')


png(file="plots/network_plot.png", width = 1000, height = 1000)
plot(
  graph,
  vertex.label = NA,
  edge.arrow.size = .25,
  vertex.size = 3,
  vertex.color = igraph::V(graph)$color
)

graphics::legend(x = 0.75, y = -.85, c("Negative","Positive", "Neutral"), pch = 21,
                 col = "#777777", pt.bg = colrs, pt.cex = 2.5, cex = 1.2, bty = "o", ncol = 1)
dev.off()
