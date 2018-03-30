#!/usr/bin/env python3

# python imports
from os import listdir, makedirs, walk, remove, getlogin
import sys
from os.path import isfile, join, exists
import subprocess
import numpy as np
import pandas as pd

# ----- Set params for this run --------------------------

# Which subjects? #
subj = ###SUB_ID###

# Which group?
conds = ###CONDS###

# Which scan number?
this_scan = 1; # sys.argv[1]
this_cond = conds[this_scan-1]

# Set projdirs dir
projdir = ###PROJ_DIR### 
subdir = join(projdir, 'data', subj)

# Set code dir
codedir = join(projdir, 'code', 'preproc', 'bash')

# Set raw dir
rawdir = join(subdir, 'raw', 'niftis_good')

# Set warp dir containing warp files
warpdir_in= join(subdir, 'preproc', 'unwarp_out')

# Set output dir for unwarping step
warpdir_out = join(subdir, 'preproc', 'unwarp_out', 'run' + str(this_scan))
if not exists(warpdir_out):
    print(warpdir_out + ' does not exist, creating')
    makedirs(warpdir_out)

# Set output dir for mc step
mcdir_out = join(warpdir_out, 'mc')
if not exists(mcdir_out):
    print(mcdir_out + ' does not exist, creating')
    makedirs(mcdir_out)

# Set output dir for fsf files
fsfdir_out = join(subdir, 'preproc', 'feat_out', 'fsf')
if not exists(fsfdir_out):
    print(fsfdir_out + ' does not exist, creating')
    makedirs(fsfdir_out)  

#------ UNWARP: B0 correction and motion correction ----------------

# EPI input
scanInfo = pd.read_csv(join(subdir, 'scanInfo.csv'), index_col=0)
epi_in = join(rawdir, scanInfo.loc[this_cond]['scanName'])

# EPI savename
epi_out = join(warpdir_out, 'run' + str(scanN) + '_unwarped.nii.gz')

# Run
print('\ngo!\n\n')
subprocess.check_call([join(codedir, 'apply_unwarp.sh'), str(scanN), warpdir_in, epi_in, epi_out])


# -----FEAT: preprocessing ------------------------------------------------------

# EPI to use in feat; output of applywarp step
epi_in = join(warpdir_out, 'run' + str(scanN) + '_unwarped.nii.gz')

# Anatomy to use in feat
anat_file = join(subdir, 'data', scanInfo.loc['anat_brain']['scanName'])

# Feat directory
preproc_dir = join(subdir, 'preproc', 'feat_out')

# FSf template
fsf_template = join(projdir, 'code', 'preproc', 'feat_template_impr.fsf')

# Run
print('\ngo!\n\n')
subprocess.check_call([join(codedir, 'run_feat.sh'), str(scanN), epi_in, anat_file, preproc_dir, fsf_template])


