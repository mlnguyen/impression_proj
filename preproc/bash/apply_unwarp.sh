#! /bin/env bash

# apply_warpCorrection
# Uses FSL's applywarp to apply B0 and motion correction to individual EPIs


# files needed
EPI_N=$1
SUB_DIR=$2
EPI_IN=$3
EPI_OUT=$4

module load fsl

# set paths
MC_DIR=${SUB_DIR}/run${EPI_N}/mc
FM_DIR=${SUB_DIR}/unwarp_files

# 1. Run motion correction using mcflirt
echo "calc motion correction xform mats for run $EPI_N with mcflirt..."
mcflirt -in $EPI_IN -out ${MC_DIR}/EPI_mcf -mats -plots -reffile ${FM_DIR}/refvol.nii.gz -spline_final
echo 'done!'
echo 

# 2. Concatenate transform matrices from mcflirt into single file
echo "concat motion correction xform mats..."
cat ${MC_DIR}/EPI_mcf.mat/MAT* > ${MC_DIR}/EPI_mcf.cat
rm -f ${MC_DIR}/EPI_mcf.nii.gz
echo 'done!'
echo

# 3. Correct EPIs for B0 distortions using fsl's applywarp
echo "applying motion correction and B0 correction ..."
applywarp -i $EPI_IN -o $EPI_OUT -r ${FM_DIR}/magnitude.nii.gz -w ${FM_DIR}/warpfield.nii.gz --premat=${MC_DIR}/EPI_mcf.cat \
    --interp=spline --paddingsize=1
echo 'done!'
echo
