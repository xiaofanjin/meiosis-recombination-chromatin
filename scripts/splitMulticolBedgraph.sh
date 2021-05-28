#!/bin/bash

fn=$1

if [ $(awk 'NR==1{print NF}' ${fn}) == 6 ]; then
	awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$4}' ${fn} > ${fn%.b*}_coverage.bg &
	awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$5}' ${fn} > ${fn%.b*}_maxScore.bg &
	awk 'BEGIN{OFS="\t"}{print $1,$2,$3,$6}' ${fn} > ${fn%.b*}_weightedScore.bg &
fi

wait
