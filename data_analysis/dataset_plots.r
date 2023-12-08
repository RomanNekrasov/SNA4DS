
fp = file.path("~/Desktop/SNA4DS/6.Project/SNA4DS/data_preparation/prepared_data/network.graphml")
main_object <- igraph::read_graph(
#  fp,
   "~/Desktop/SNA4DS/6.Project/SNA4DS/data_preparation/prepared_data/network.graphml",
  format = "graphml"
)

main_graph <- main_object

# Centralities Plot
# Save a plot of centrlaity measures (betweenness, closeness, degree, eccentricity)
png(file="plots/centralities_plot.png", width = 600, height = 1000)
(centralities_plot <- snafun::plot_centralities(
  graph,
  measures = c("betweenness", "closeness", "degree", "eccentricity"), 
  directed = TRUE,
  mode = "all",
  k = 3,
  rescaled = FALSE
))
dev.off()


# Degree Distribution Plot
# Calculate and save a frequency plot of the degree distribution for the entire graph
degree_distribution <- snafun::g_degree_distribution(graph, 
    mode = "all", 
    type = "count")

png(file="plots/degree_distr.png", width = 600, height = 400)
# Create a frequency plot with lines
plot(1:length(degree_distribution), degree_distribution, type = "h", lwd = 2, 
     main = "Degree Distribution", xlab = "Degree", ylab = "Frequency")
dev.off()

# In Degree Distribution Plot
# Calculate and save a frequency plot of the in-degree distribution for the graph
degree_distribution <- snafun::g_degree_distribution(graph, 
    mode = "in", 
    type = "count")

png(file="plots/indegree_distr.png", width = 600, height = 400)
# Create a frequency plot with lines
plot(1:length(degree_distribution), degree_distribution, type = "h", lwd = 2, 
     main = "In Degree Distribution", xlab = "inDegree", ylab = "Frequency")
dev.off()

# Out Degree Distribution Plot
# Calculate and save a frequency plot of the out-degree distribution for the graph
degree_distribution <- snafun::g_degree_distribution(graph, 
    mode = "out", 
    type = "count")

png(file="plots/outdegree_distr.png", width = 600, height = 400)
# Create a frequency plot with lines
plot(1:length(degree_distribution), degree_distribution, type = "h", lwd = 2, 
     main = "Out Degree Distribution", xlab = "outDegree", ylab = "Frequency")
dev.off()
