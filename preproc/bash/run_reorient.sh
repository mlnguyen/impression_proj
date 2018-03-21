#! /bin/env bash

module load fsl

# arguments
T1_ORIG=$1
T1_REORIENT=$2

# Reorient 
echo 'reorient brain to std ...'
fslreorient2std $T1_ORIG $T1_REORIENT
echo 'done!'

