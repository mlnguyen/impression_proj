
#!/usr/bin/env python3

# STEP 2 -------------------------------------------------
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
import matplotlib.pyplot as plt
import shutil
import pandas as pd
import socket
from nilearn import image, plotting

# SETUP ---------------------------------------------------
# set subject specific info
subj = ###SUB_ID###
last_scan = ###REF_SCAN###

# Set projdirs dir
projdir = '/mnt/bucket/labs/hasson/mai/projects/impressions'
datadir = join(projdir, 'data')
acqdir = join(projdir, 'acq_params')

# Set code dir
codedir = join(projdir, 'code', 'preproc', 'bash')

# Rawdir
rawdir = join(datadir, subj, 'raw', 'niftis_good')

# Set acqparams file
acqparams_file = join(acqdir, 'acqparams.txt')

# Set config file
config_file = join(acqdir, 'b02b0.cnf')

# Load scan info
scanInfo = pd.read_csv(join(datadir, subj, 'scanInfo.csv'), index_col=0)
print(scanInfo)


# CREATE FIELDMAPS USING FSL'S TOPUP FX -----------------------------
# 1. Merges SE fieldmaps into single file
# 2. Run's FSL topup fx to correct the fieldmaps
# 3. Convert corrected fieldmaps to magnitude map by taking average
# 4. Convert corrected phase map in Hz to phase map in rads    

# create output dir
outdir = join(datadir, subj, 'preproc', 'unwarp_out', 'unwarp_files')
fm_outdir = join(outdir, 'fieldmap_figures')
bet_outdir = join(outdir, 'bet_figures')
if not exists(outdir):
    print(outdir + ' does not exist, creating')
    makedirs(outdir)
if not exists(fm_outdir):
    print(fm_outdir + ' does not exist, creating')
    makedirs(fm_outdir)
if not exists(bet_outdir):
    print(bet_outdir + ' does not exist, creating')
    makedirs(bet_outdir)
    
    
# set fieldmap dir and files
raw_nifti_dir = join(datadir, subj, 'raw', 'niftis_good')
fieldmap_ap = join(raw_nifti_dir, scanInfo.loc['se_fieldmap_ap']['scanName'])
fieldmap_pa = join(raw_nifti_dir, scanInfo.loc['se_fieldmap_pa']['scanName'])
ref_epi = join(raw_nifti_dir, scanInfo.loc[last_scan]['scanName'])

# run topup
get_ipython().system("{join(codedir, 'prep_unwarpFiles.sh')} {outdir} {fieldmap_ap} {fieldmap_pa} 
                      {acqparams_file} {config_file} {ref_epi}")


# MAKE FIELDMAP FIGURES ----------------------------------------------

# Original SE maps
fieldmap = join(outdir, 'concat_fieldmaps.nii.gz')
print('saving images of original SE maps...')
for i in range(3):
    plot_title = 'orig_se_ap_' + str(i)
    plotting.plot_anat(image.index_img(fieldmap,i), dim=-1, title=plot_title, 
                       output_file = join(fm_outdir, plot_title + '.png'))
for i in range(3,6):
    plot_title = 'orig_se_pa_' + str(i)
    plotting.plot_anat(image.index_img(fieldmap,i), dim=-1, title=plot_title, 
                       output_file = join(fm_outdir, plot_title + '.png'))

# Corrected SE maps
fieldmap = join(outdir, 'topup_iout.nii.gz')
print('saving images of corrected SE maps...')
for i in range(3):
    plot_title = 'corr_se_ap_' + str(i)
    plotting.plot_anat(image.index_img(fieldmap,i), dim=-1, title=plot_title, 
                       output_file = join(fm_outdir, plot_title + '.png'))
for i in range(3,6):
    plot_title = 'corr_se_pa_' + str(i)
    plotting.plot_anat(image.index_img(fieldmap,i), dim=-1, title=plot_title, 
                       output_file = join(fm_outdir, plot_title + '.png'))
    
# Check magnitude and phase maps
print('saving images of phase and magnitue maps...')
plotting.plot_anat(join(outdir, 'magnitude.nii.gz'), dim=-1, title='mag map', 
                  output_file = join(fm_outdir, 'mag_map_mean.png'))
plotting.plot_anat(join(outdir, 'magnitude_brain.nii.gz'),  dim=-1, title='mag map brain', 
                  output_file = join(fm_outdir, 'mag_map_brain.png'))
plotting.plot_anat(join(outdir, 'topup_fout.nii.gz'),  dim=0, title='phase map', 
                   output_file = join(fm_outdir, 'phase_map.png'))







