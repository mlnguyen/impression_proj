#! /bin/env bash

module load fsl

# arguments
T1_ORIG=$1
T1_REORIENT=$2
T1_BRAIN=$3

# Reorient 
echo 'reorient brain to std ...'
fslreorient2std $T1_ORIG $T1_REORIENT
echo 'done!'
echo

# Run bet
echo 'extracting brain using bet ...'
bet $T1_REORIENT $T1_BRAIN -f 0.5 -g 0 -B
echo 'done!'
echo
