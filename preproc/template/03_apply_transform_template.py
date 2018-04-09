#!/usr/bin/env python3

# --------------------------------------------------------------------------------
# 03_apply_transform.py
#    1. Applies subject--> MNI standard transform using fsl's flirt
#    2. Copies and renames processed niftis
# -------------------------------------------------------------------------------

# python imports
from os import listdir, makedirs
import sys
from os.path import isfile, join, exists
import subprocess
import numpy as np
import pandas as pd

# Set params for experiment --------------------------------------------------------
print('\n\nsetting up params...')

# Which subjects? #
subj = ###SUB_ID###

# Set projdirs dir
subdir = ###SUB_DIR###

# Set codedir
codedir =  ###CODE_DIR###

# Set refdirs
refbrain =  ###REF_BRAIN###

# Do transform --------------------------------------------------------------------
print('starting transforms...\n')

# load scanInfo
scanInfo = pd.read_csv(join(subdir, 'scanInfo.csv'), index_col=0)
epiInfo = scanInfo[scanInfo['scanType']=='epi']

this_scan = int(sys.argv[1])
scanInfo = epiInfo.iloc[this_scan-1]

print('applying transform to ' + scanInfo['preprocDir'] + '...')
feat_outdir = join(subdir, 'preproc', 'feat_out', scanInfo['preprocDir']+'.feat')
orig_nifti = join(feat_outdir, 'filtered_func_data.nii.gz')
out_nifti = join(subdir, 'data','niftis', subj + '_epi_' + scanInfo['scanCond'] + '.nii.gz')

output = subprocess.check_output([join(codedir, 'apply_transform.sh'), orig_nifti,
 				out_nifti, feat_outdir, refbrain])
