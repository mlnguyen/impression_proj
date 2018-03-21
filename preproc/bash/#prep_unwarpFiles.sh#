#! /bin/env bash

# prep_fieldmapFiles
# Uses FSL's topup to prep files for fieldmap correction

#SBATCH -J 'prep_fieldmapFiles'
#SBATCH -o log/topup-%j.log
#SBATCH -p all
#SBATCH --mem=4GB
#SBATCH -t 70

OUT_DIR=$1
AP_FILE=$2
PA_FILE=$3
ACQ_FILE=$4
CNF_FILE=$5
REF_EPI=$6

echo "output path for files: $OUT_DIR"
echo "input_AP: $AP_FILE"
echo "input_PA: $PA_FILE"
echo "input acq file: $ACQ_FILE"
echo "input cnf file: $CNF_FILE"
echo "input ref epi: $REF_EPI"
echo
echo

module load fsl

# 1. Concatenate fieldmaps into single file, concat_fieldmaps using fslmerge
echo 'concatenating se fielmdaps ...'
if [ -e ${OUT_DIR}/concat_fieldmaps.nii.gz ]
then
    echo 'concat_fieldmaps exists, skipping step'
else
    fslmerge -t ${OUT_DIR}/concat_fieldmaps.nii.gz ${AP_FILE} ${PA_FILE}
fi
echo 'done!'
echo 

# 2. Run top up to make fieldmap files.
# Topup params:
#       --imagain = concatenated fieldmap
#       --datain  = data acqparams file
#       --config  = configuraation file, .cnf, from fsl
#       --out     = basename for files produced by topup
#       --iout    = name of 4D image that contains unwarped/movement corrected files
#       --fout    = name of outfile containing estimated fieldmap in Hz
#       --logout  = name of outputfile containing log 
echo 'running topup to create fieldmap files ...'
if [ -e ${OUT_DIR}/topup_iout ]
then
    echo 'topup already run, skipping step'
else
    topup --imain=${OUT_DIR}/concat_fieldmaps --datain=${ACQ_FILE} --config=${CNF_FILE} --out=${OUT_DIR}/topup_output \
	--iout=${OUT_DIR}/topup_iout --fout=${OUT_DIR}/topup_fout --logout=${OUT_DIR}/topup_logout
fi
echo 'done!'
echo 

# 3. Create magnitude fieldmap: get average of corrected SE maps using fslmaths
echo 'calc mean map...'
if [ -e ${OUT_DIR}/magnitude ]
then
    echo 'mean magnitude map exists already, skipping step'
else
    fslmaths ${OUT_DIR}/topup_iout -Tmean ${OUT_DIR}/magnitude
fi
echo 'done!'
echo 

#4. Extract brain from mean mag map
echo 'extracting brain from mean mag map using Bet'
if [ -e ${OUT_DIR}/magnitude_brain ]
then
    echo 'mean mag brain map exists already, skipping step'
else
    bet ${OUT_DIR}/magnitude ${OUT_DIR}/magnitude_brain
fi
echo 'done!'
echo

# 4. Convert phase map in Hz to pixel shift map
echo 'converting phase map to pixel shift map...'
if [ -e ${OUT_DIR}/shiftmap.nii.gz ]
then
    echo 'shiftmap already exists, skipping step'
else
    fslmaths ${OUT_DIR}/topup_fout -mul .0665 ${OUT_DIR}/shiftmap.nii.gz
fi
echo 'done'
echo 

# 5. Convert pixel shift map into a deformation (warp map)
echo 'converting pixel-shift map into warp map...'
if [ -e ${OUT_DIR}/warpfield ]
then
    echo 'warp map already exists, skipping step'
else
    convertwarp -r ${OUT_DIR}/magnitude.nii.gz -s ${OUT_DIR}/shiftmap.nii.gz -o ${OUT_DIR}/warpfield.nii.gz -d y
fi
echo 'done!'
echo 

# 6. Extract reference EPI volume for motion correction
echo 'extracting reference vol for motion correction...'
if [ -e ${OUT_DIR}/refvol.nii.gz ]
then
    echo 'ref vol already exists, skipping step'
else
    fslroi $REF_EPI ${OUT_DIR}/refvol.nii.gz 0 1
fi
echo done!
echo

echo done and done


