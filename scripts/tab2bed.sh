#!/bin/bash
inputTab=$1
outputBed=$2

awk 'BEGIN{OFS="\t"}NR>1{print $2,$3,$4,1/($7+1)}' ${inputTab} | sort -k1,1V -k2,2V > ${outputBed}
