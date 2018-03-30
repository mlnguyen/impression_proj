#! /bin/env bash

module load fsl

# arguments
T1_ORIG=$1
T1_REORIENT=$2
ANAT_DIR=$3
CUR_DIR=$PWD

# Reorient 
echo 'reorient brain to std ...'
fslreorient2std $T1_ORIG $T1_REORIENT
echo 'done!'

# Brain extraction
echo 'launch brain extraction gui ...'
#cd $ANAT_DIR
#Bet &
#fslview &
#cd $CUR_DIR
echo 'done!'
