#!/bin/bash

DIRNAME=$(dirname "$0")
echo $(date "+%m/%d/%y %H:%M:%S"),start,$1 >> $DIRNAME/statistik.csv