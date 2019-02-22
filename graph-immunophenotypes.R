library(tidyverse)
library(ggraph)
library(igraph)
library(ggrepel)

parent_child <- read_csv("example-phenotype-list.csv") %>%
  mutate(phenotype_depth = str_count(immunophenotype, " ")) %>%
  arrange(phenotype_depth)

network_frame <- data.frame()

for(depth in unique(parent_child$phenotype_depth)){
  current_depth <- depth
  deeper_depth <- depth + 1
  if(deeper_depth > max(unique(parent_child$phenotype_depth))){
    break
  }
  
  sep_col_names <- paste0("marker_", c(1:deeper_depth))
  
  parent_pops <- parent_child %>%
    filter(phenotype_depth == current_depth) %>%
    transmute(parent_immunophenotype = immunophenotype) %>%
    separate(parent_immunophenotype, into = sep_col_names, sep = " ", remove = F) %>%
    gather(marker_number,
           immunophenotype,
           starts_with("marker_")) %>%
    select(-marker_number)
  
  sep_col_names <- paste0("marker_", c(0:deeper_depth))
  
  child_pops <- parent_child %>%
    filter(phenotype_depth == deeper_depth) %>%
    transmute(child_immunophenotype = immunophenotype) %>%
    separate(child_immunophenotype, into = sep_col_names, sep = " ", remove = F) %>%
    gather(marker_number,
           immunophenotype,
           starts_with("marker_")) %>%
    select(-marker_number)
  
  parent_child_linked <- parent_pops %>%
    left_join(child_pops) %>%
    count(parent_immunophenotype, child_immunophenotype) %>%
    filter(n == deeper_depth)
 
  network_frame <- bind_rows(network_frame, parent_child_linked) 
}

gr <- graph_from_data_frame(network_frame)  

decompose.graph(gr)[[2]] %>%
  ggraph(layout = 'kk') +
  geom_node_point() + 
  geom_edge_link(color = "grey", arrow = arrow(length = unit(4, 'mm')))

graph <- graph_from_data_frame(flare$edges, vertices = flare$vertices)

decompose.graph(gr)[[2]] %>%
  ggraph('circlepack') + 
  geom_node_circle(aes(fill = depth), size = 0.25, n = 50) + 
  geom_node_label(aes(label = name, position = "repel")) + 
  coord_fixed()
ggsave("test_dag_plot.png")

decompose.graph(gr)[[2]] %>%
  create_layout('circlepack')
