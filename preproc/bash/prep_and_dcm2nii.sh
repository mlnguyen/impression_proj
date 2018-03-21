#! /bin/env bash

RAWDIR=$1
OUTDIR=$2

module load mricrogl

# copy files from rawdir ($1) to outdir ($2)
echo 'copying dicoms'
cp $RAWDIR/*.dcm* $OUTDIR
echo

# unzip
echo 'unzipping dicoms'
gunzip $OUTDIR/*.gz
echo

# convert to nifti
echo 'converting dicms to nifti'
dcm2niix  -z y -f %2s_%p $OUTDIR
echo

# delete dicoms from outpudir
echo 'deleting old dcms'
rm -f $OUTDIR/*.dcm

