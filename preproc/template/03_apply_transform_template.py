#!/usr/bin/env python3

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

for ind,row in epiInfo.iterrows():

	print('applying transform to ' + row['preprocDir'] + '...')
	feat_outdir = join(subdir, 'preproc', 'feat_out', row['preprocDir']+'.feat')
	orig_nifti = join(feat_outdir, 'filtered_func_data.nii.gz')
	out_nifti = join(subdir, 'data', subj + '_epi_' + row['scanCond'] + '.nii.gz')

	output = subprocess.check_output([join(codedir, 'apply_transform.sh'), orig_nifti,
 				out_nifti, feat_outdir, refbrain])


	print('\n')
