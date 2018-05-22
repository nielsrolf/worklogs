#!/bin/bash
echo $(date "+%m/%d/%y %H:%M:%S"),stop,->> statistik.csv
python statistik.py 
