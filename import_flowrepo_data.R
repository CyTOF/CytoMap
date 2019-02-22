library(FlowRepositoryR)

#List of flow data sets
#Column 1 is a high level descriptor, e.g. mice
#Column 2 is the FlowRepo id
flow_data <- read.csv("flow-datasets.csv",header = F,stringsAsFactors = F)

for (i in 1:nrow(flow_data)){
  ds <- flowRep.get(flow_data$V2[i])
  download(ds,dirpath=paste0("data/cytof/",flow_data$V1[i],"/",flow_data$V2[i]))
}
 
