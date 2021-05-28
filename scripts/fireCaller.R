#!/usr/bin/Rscript
args = commandArgs(trailingOnly=TRUE)
folder = args[1]
map_file = args[2]
library("FIREcaller")
setwd(folder)
prefix.list <- c('rawMatrix')
gb<-'mm10'
rm_mhc <- FALSE

FIREcaller(prefix.list, gb, map_file, rm_mhc)
