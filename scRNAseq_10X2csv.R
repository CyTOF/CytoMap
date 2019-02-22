require(Matrix)
args = commandArgs(trailingOnly=TRUE)
require("optparse")
option_list = list(
  make_option(c("-i", "--input"), type="character", default="~/"),
  make_option(c("-o", "--output"), type="character", default="count.csv")
); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

matrix_dir = opt$input
matrix_out = opt$output

barcode.path = paste0(matrix_dir, list.files(path = matrix_dir, pattern = "*barcodes*"))
features.path = paste0(matrix_dir, list.files(path = matrix_dir, pattern = "*genes*"))
matrix.path = paste0(matrix_dir, list.files(path = matrix_dir, pattern = "*mtx*"))
ma = readMM(file = matrix.path[1])
feature.names = read.delim(features.path[1], header = FALSE, stringsAsFactors = FALSE)
barcode.names = read.delim(barcode.path[1], header = FALSE,stringsAsFactors = FALSE)
colnames(ma) = barcode.names$V1
rownames(ma) = feature.names$V1
for (i in 2:length(barcode.path)){
    mat = readMM(file = matrix.path[i])
    feature.names = read.delim(features.path[i], header = FALSE, stringsAsFactors = FALSE)
    barcode.names = read.delim(barcode.path[i], header = FALSE,stringsAsFactors = FALSE)
    colnames(mat) = barcode.names$V1
    rownames(mat) = feature.names$V1
    if (sum(rownames(mat) == rownames(ma)) == nrow(ma)){
      ma = cbind(ma, mat[rownames(ma),])
    }
    else{print("Genes not same.")}
}

write.csv(as.matrix(ma), paste0(matrix_dir, matrix_out))