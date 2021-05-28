#!/bin/bash

binBed=$1
trackBed=$2
outBed=$3

#if bedgraph, bin with 3 columns (can split using splitMulticolBedgraph.sh): coverage, max score, coverage-weighted score
#if bed, bin and report coverage
if [ $(awk 'NR==1{print NF}' ${trackBed}) == 4 ]; then \
	bedtools intersect -a ${binBed} -b ${trackBed} -wao | \
	awk 'BEGIN{OFS="\t"}NR==1{binSize=$3-$2}{if($7=="."){print $1,$2,$3,0,0,0}else{print $1,$2,$3,$7,$8,$7*$8/binSize}}' | \
	bedtools merge -c 5,4,6 -o sum,max,sum -d -1 > ${outBed}
elif [ $(awk 'NR==1{print NF}' ${trackBed}) == 3 ]; then \
	bedtools intersect -a ${binBed} -b ${trackBed} -wao | \
	awk 'BEGIN{OFS="\t"}NR==1{binSize=$3-$2}{print $1,$2,$3,$7/binSize}' | \
	bedtools merge -c 4 -o sum -d -1 > ${outBed}
fi
