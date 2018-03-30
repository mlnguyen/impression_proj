
#!/usr/bin/env python3

# STEP 1 -------------------------------------------------
# Prepare various files for doing preprocessing:
# 1. Prep unwarp files: 
#     * create fieldmaps for B0 correction
# 2. Extract ref vol for motion correction
# -------------------------------------------------------

# python imports
from os import listdir, makedirs, walk, remove, getlogin
from os.path import isfile, join, exists
import subprocess
import numpy as np
import shutil
import pandas as pd
from nilearn import image, plotting
import subprocess

# SETUP ---------------------------------------------------
# set subject specific info
subj = ###SUB_ID###
last_scan = ###REF_SCAN###

# Set projdirs dir
projdir = ###PROJ_DIR### 
datadir = join(projdir, 'data')
acqdir = join(projdir, 'acq_params')

# Set code dir
codedir = join(projdir, 'code', 'preproc', 'bash')

# Rawdir
rawdir = join(datadir, subj, 'raw', 'nii')

# Set acqparams file
acqparams_file = join(acqdir, 'acqparams.txt')

# Set config file
config_file = join(acqdir, 'b02b0.cnf')

# Load scan info
scanInfo = pd.read_csv(join(datadir, subj, 'scanInfo.csv'), index_col=0)


# CREATE FIELDMAPS USING FSL'S TOPUP FX -----------------------------
# 1. Merges SE fieldmaps into single file
# 2. Run's FSL topup fx to correct the fieldmaps
# 3. Convert corrected fieldmaps to magnitude map by taking average
# 4. Convert corrected phase map in Hz to phase map in rads    

# create output dir
outdir = join(datadir, subj, 'preproc', 'unwarp_out', 'unwarp_files')
fm_outdir = join(outdir, 'fieldmap_figures')
if not exists(outdir):
    print(outdir + ' does not exist, creating')
    makedirs(outdir)
if not exists(fm_outdir):
    print(fm_outdir + ' does not exist, creating')
    makedirs(fm_outdir)
    
    
# set fieldmap dir and files
fieldmap_ap = join(rawdir, scanInfo.loc['se_fieldmap_ap']['niftiName'])
fieldmap_pa = join(rawdir, scanInfo.loc['se_fieldmap_pa']['niftiName'])
ref_epi = join(rawdir, scanInfo.loc[last_scan]['niftiName'])

# run topup
print('\nrunning topup...\n')
subprocess.check_call([join(codedir, 'prep_unwarpFiles.sh'), outdir, fieldmap_ap, fieldmap_pa,
				 acqparams_file, config_file, ref_epi])



