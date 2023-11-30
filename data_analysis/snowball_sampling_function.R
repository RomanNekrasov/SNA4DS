# This code was  adaped from: https://rdrr.io/cran/netdep/src/R/snowball.R
# only thing changed is mode parameter in line 30 and in function input

# snowball.sampling function performs snowball sampling on a graph.
# G: The graph on which sampling is to be performed.
# samn: The number of samples to be collected.

library(igraph)

snowball.sampling = function(G, samn, adjacent_mode = 'out') {
  
  # Check if the population size is less than the sample size
  if (vcount(G) < samn) {
    return("Population size is not enough for snowball sampling")
  }
  
  ind = c()
  V(G)$name = c(1:vcount(G))  # Assign names from 1 to number of vertices
  starter = sample(V(G)$name, 1)  # Sample from vertex names
  current = c()
  current[1] = starter  # Use the name directly
  count = 1
  ind[1] = current[1]
  
  # Continue sampling until the sample number is reached
  while (count < samn) {
    nnode = length(current)  # Number of subjects in the current stage
    for (i in 1:nnode) {
      # Fetch neighbors by vertex name, not index
      ngh = neighbors(G, current[i], mode = adjacent_mode) 
      ind = c(ind, V(G)$name[ngh])
      ind = unique(ind)
    }
    tmp_sample = ind[(count + 1):length(ind)]
    
    # Adjust if the sampled size exceeds the target
    if (samn < length(ind)) {
      need = samn - count  # Number of subjects needed
      tmp_sample = sample(tmp_sample, need)
      ind[(count + 1):samn] = tmp_sample
      ind = ind[-c((samn + 1):length(ind))]
    }
    current = tmp_sample
    count = length(ind)
  }
  
  # Return the subgraph and indices if successful
  if (count == samn) {
    # Create the subgraph using vertex names
    subG = induced.subgraph(G, which(V(G)$name %in% ind))
    return(list(subG = subG, ind = ind))
  } else {
    return("Something goes wrong.")
  }
}
