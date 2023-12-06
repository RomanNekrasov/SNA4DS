
fp = file.path("data_preparation/prepared_data/network.graphml")
main_object <- igraph::read_graph(
  fp,
#   '/Users/huubvandevoort/Desktop/SNA4DS/6. Project/SNA4DS/data_preparation/prepared_data/network.graphml',
  format = "graphml"
)

graph <- main_object

# Centralities Plot
png(file="plots/centralities_plot.png", width = 600, height = 1000)
snafun::plot_centralities(
  graph,
  measures = c("betweenness", "closeness", "degree", "eccentricity"), 
  directed = TRUE,
  mode = "all",
  k = 3,
  rescaled = FALSE
)
dev.off()


# Degree Plots
degree_distribution <- snafun::g_degree_distribution(graph, 
    mode = "out", 
    type = "count")

png(file="plots/outdegree_distr.png", width = 600, height = 400)
# Create a frequency plot with lines
plot(1:length(degree_distribution), degree_distribution, type = "h", lwd = 2, 
     main = "Degree Distribution", xlab = "outDegree", ylab = "Frequency")
dev.off()

