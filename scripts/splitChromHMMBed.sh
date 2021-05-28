#!/bin/bash
inputFile=$1

for state in $(awk '{print $4}' ${inputFile} | sort | uniq); do awk -v state="${state}" 'BEGIN{OFS="\t"}$4==state{print $1,$2,$3}' ${inputFile} > ${inputFile%.bed}_state_${state}.bed; done
