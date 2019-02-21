library(FlowRepositoryR)

flow_data <- read.csv("flow-datasets.txt",header = F,stringsAsFactors = F)

for (ds.name in flow_data$V1){
  ds <- flowRep.get(ds.name)
  download(ds,dirpath=paste0("data/cytof/",ds.name))
}
 
