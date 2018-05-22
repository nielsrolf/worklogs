#!/bin/bash

DIRNAME=$(dirname "$0")

echo $(date "+%m/%d/%y %H:%M:%S"),stop,->> $DIRNAME/statistik.csv
python $DIRNAME/statistik.py 
