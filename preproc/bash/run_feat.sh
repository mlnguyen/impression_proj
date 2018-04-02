#! /bin/env bash

module load fsl

# rename arguments
RUN_NAME=$1
EPI_FILE=$2
ANAT_FILE=$3
PREPROC_DIR=$4
FSF_TEMPLATE=$5


# Set usueful vars
FSF_FILE=${PREPROC_DIR}/fsf/${RUN_NAME}.fsf
FEAT_OUT_DIR=${PREPROC_DIR}/${RUN_NAME}.feat

# get number of volumes for this run
N_VOLS=$(fslnvols $EPI_FILE)

# Create fsf for this run from fsf template
echo "create fsf file for $RUN_NAME ..."
sed -e "s@###INPUTDIR###@${EPI_FILE}@g" \
	-e "s@###ANATDIR###@${ANAT_FILE}@g" \
	-e "s@###NVOLS###@${N_VOLS}@g" \
	-e "s@###OUTPUTDIR###@${FEAT_OUT_DIR}@g" \
	${FSF_TEMPLATE} > ${FSF_FILE}

echo "running feat job..."
feat ${FSF_FILE}
