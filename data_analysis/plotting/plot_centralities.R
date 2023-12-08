igraph::V(graph)$color <- "black"
igraph::V(graph) [ sentiment == 'negative' ]$color <- "#F25F5C"
igraph::V(graph) [ sentiment == 'positive' ]$color <- "#9DBF9E"
igraph::V(graph) [ sentiment == 'neutral' ]$color <- "black"

my_df <- data.frame(
  igraph::get.vertex.attribute(graph, name = "id"), 
  igraph::get.vertex.attribute(graph, name = "color"),
  1:324
  )

# v_degree <- snafun::v_degree(graph, mode = "out", )
v_degree <- igraph::degree(graph, mode = "out")
# names(v_degree) <- "degree"

# my_df[is.na(my_df)] <- 0

my_df <- cbind(my_df, v_degree)

names(my_df) <- c("id", "color", "new_id", "degree")

plot(y = my_df$new_id, 
     x = my_df$degree, 
     col = my_df$color,
     type = "b",
     pch = 16)
