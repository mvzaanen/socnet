#!/bin/bash

# for mac:
# export LC_LANG=en_US.UTF-8

file=war_and_peace1000
#file=war_and_peace

# Extract NE
./NE_extractor.py \
  -i ${file}.txt \
  -e ${file}_edges.csv \
  -n ${file}_nodes.csv

## Check text against "regular" words
#./NE_check.py \
#  -i ${file}.txt \
#  -o ${file}_ne_check.txt

## Dependency parsing
#./NE_depparse.py \
#  -i ${file}.txt \
#  -n ${file}_ne.txt \
#  -o ${file}_dep.txt

# Identify sentences with multiple NE
#./identify_NE_sentences.py \
#  -i ${file}.txt \
#  -n ${file_}names_only.txt \
#  -o ${file}_multiple_ne.txt
