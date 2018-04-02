#!/bin/bash
#
# apply_transform.sh
# Applies non-linear transformation to subject EPI, moving from subject space to 3mm MNI
# space. Assumes subject EPI was generated using FLIRT followed by FNIRT.

module load fsl

NIFTI_IN=$1
NIFTI_OUT=$2
FEAT_DIR=$3
MNI_BRAIN=$4

# Apply transformations: subject space --> MNI 3mm
echo 'applying transform...'

WARP_FILE=$FEAT_DIR/reg/highres2standard_warp
TRANS_MAT=$FEAT_DIR/reg/example_func2highres.mat

applywarp --ref=$MNI_BRAIN --in=$NIFTI_IN --out=$NIFTI_OUT --warp=$WARP_FILE --premat=$TRANS_MAT

echo 'done!'
