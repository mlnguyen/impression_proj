#! /bin/env bash

module load fsl

# rename arguments
RUN_NUM=$1
EPI_FILE=$2
ANAT_FILE=$3
PREPROC_DIR=$4
FSF_TEMPLATE=$5


# Set usueful vars
FSF_FILE=${PREPROC_DIR}/fsf/run${RUN_NUM}.fsf
FEAT_OUT_DIR=${PREPROC_DIR}/run${RUN_NUM}.feat

# get number of volumes for this run
N_VOLS=$(fslnvols $EPI_FILE)

# Create fsf for this run from fsf template
echo "create fsf file for run $RUN_NUM ..."
sed -e "s@###INPUTDIR###@${EPI_FILE}@g" \
	-e "s@###ANATDIR###@${ANAT_FILE}@g" \
	-e "s@###NVOLS###@${N_VOLS}@g" \
	-e "s@###OUTPUTDIR###@${FEAT_OUT_DIR}@g" \
	${FSF_TEMPLATE} > ${FSF_FILE}
echo 'done'
echo

echo "run feat..."
feat ${FSF_FILE}
echo "done"

echo "done and done"
