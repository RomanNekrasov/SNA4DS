graph <- igraph::read_graph(
  '/Users/huubvandevoort/Desktop/SNA4DS/6. Project/SNA4DS/data_preparation/prepared_data/network.graphml',
  format = "graphml"
)

# # Generate colors based on year:
colrs <- c("red", "green", "orange", "purple")
# # create a new attribute with the color
# igraph::V(graph)$color <- colrs[igraph::V(graph)$sentiment] # we attribute each year to a color
library(igraph)

igraph::V(graph)$membership <- membership(edge.betweenness.community(graph))
igraph::V(graph)$color == "black"
igraph::V(graph) [ sentiment == 'negative' ]$color <- "blue"
igraph::V(graph) [ sentiment == 'positive' ]$color <- "green"
igraph::V(graph) [ sentiment == 'neutral' ]$color <- "brown"
igraph::V(graph) [ sentiment == 'no sentiment' ]$color <- "orange"

#pal <- c("red", "green", "orange", "purple")
#vertex_colors <- pal[igraph::V(graph)$sentiment]


plot(
  graph,
  vertex.label = NA,
  edge.arrow.size = .1,
  vertex.size = 3,
  vertex.color=igraph::V(graph)$color,
  layout=layout.sphere
#  vertex.size=igraph::V(graph)$average_length_comments*0.08,
#  layout=layout.fruchterman.reingold
)


graphics::legend(x = -1.5, y = -1.1, c("negative","positive", "neutral", "no sentiment"), pch = 21,
                 col = "#777777", pt.bg = colrs, pt.cex = 2, cex = .8, bty = "n", ncol = 1)
