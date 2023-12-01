fp = file.path('data_preparation', 'prepared_data', 'network.graphml')
graph <- igraph::read_graph(
  fp,
#   '/Users/huubvandevoort/Desktop/SNA4DS/6. Project/SNA4DS/data_preparation/prepared_data/network.graphml',
  format = "graphml"
)

# # Generate colors based on year:
colrs <- c("red", "green", "orange", "purple")


igraph::V(graph)$color == "black"
igraph::V(graph) [ sentiment == 'negative' ]$color <- "blue"
igraph::V(graph) [ sentiment == 'positive' ]$color <- "green"
igraph::V(graph) [ sentiment == 'neutral' ]$color <- "brown"
igraph::V(graph) [ sentiment == 'no sentiment' ]$color <- "orange"

#pal <- c("red", "green", "orange", "purple")
#vertex_colors <- pal[igraph::V(graph)$sentiment]

igraph::V(graph)$membership <- membership(edge.betweenness.community(graph))
igraph::V(graph)$stress = snafun::v_stress(graph, igraph::V(graph))
igraph::V(graph)$eccentricity <- igraph::eccentricity(graph, 
                                                      vids = igraph::V(graph),
                                                      mode = 'all')


plot(
  graph,
  vertex.label = NA,
  edge.arrow.size = .1,
  vertex.size = igraph::V(graph)$eccentricity/2,
  vertex.color = igraph::V(graph)$color
)


graphics::legend(x = -1.5, y = -1.1, c("negative","positive", "neutral", "no sentiment"), pch = 21,
                 col = "#777777", pt.bg = colrs, pt.cex = 2, cex = .8, bty = "n", ncol = 1)
