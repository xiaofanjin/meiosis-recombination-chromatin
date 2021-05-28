#!/bin/bash
coolerFile=$1
mapFile=$2

coolerFolder=$(dirname ${coolerFile})
coolerPrefix=$(basename ${coolerFile%.*})
mkdir -p ${coolerFolder}/${coolerPrefix}_fireAnalysis
python makeMatrixFiles.py ${coolerFile} ${coolerFolder}/${coolerPrefix}_fireAnalysis 
for fn in $(ls ${coolerFolder}/${coolerPrefix}_fireAnalysis/rawMatrix*)
do gzip ${fn}
done
Rscript fireCaller.R ${coolerFolder}/${coolerPrefix}_fireAnalysis ${mapFile}
awk 'BEGIN{OFS="\t"}NR>1{print $1,$2,$3,$4}' ${coolerFolder}/${coolerPrefix}_fireAnalysis/FIRE_ANALYSIS_5KB.txt > ${coolerFolder}/${coolerPrefix}_fireScore.bg
rm -r ${coolerFolder}/${coolerPrefix}_fireAnalysis/
