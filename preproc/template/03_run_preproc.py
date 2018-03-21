
#!/usr/bin/env python3


# python imports
from os import listdir, makedirs, walk, remove, getlogin
import sys
from os.path import isfile, join, exists
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import shutil
import pandas as pd
import socket
from nilearn import image, plotting

# ----- Set params for this run --------------------------

# Which subjects? #
subj = ###SUB_ID###

# Which group?
conds = ###CONDS###

# Which scan number?
this_scan = 1; # sys.argv[1]
this_cond = conds[this_scan-1]

# Set projdirs dir
projdir = '/mnt/bucket/labs/hasson/mai/projects/impressions'
subdir = join(projdir, 'data', subj)

# Set code dir
codedir = '/mnt/bucket/labs/hasson/mai/projects/impressions/code/preproc/bash'

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
get_ipython().system("{join(codedir, 'apply_unwarp.sh')} {str(scanN)} {warpdir_in} {epi_in} {epi_out}")


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
get_ipython().system("{join(codedir, 'run_feat.sh')} {str(scanN)} {epi_in} {anat_file} {preproc_dir} {fsf_template}")


# ------  Make images to check unwarping ------------------------------------------------
img_savedir = join(warpdir_out, 'unwarp_figures')
if not exists(img_savedir):
    makedirs(img_savedir)

# mean map, before unwarping
plotting.plot_epi(image.mean_img(join(rawdir, scanInfo.loc[this_cond]['scanName'])), 
                  title=this_cond + '_mean_raw', cmap='gray', 
                  output_file=join(img_savedir, this_cond + '_mean_raw.png'))
# mean map, after unwarping
plotting.plot_epi(image.mean_img(join(warpdir_out, 'run' + str(scanN) + '_unwarped.nii.gz')), 
                  title=this_cond + '_mean_unwarp', cmap='gray', 
                  output_file=join(img_savedir, this_cond + '_mean_raw.png'))

# ----- Motion results ------------------------------------------------------------------
mc_file = open(join(warpdir_out, 'mc', 'EPI_mcf.par'), 'r')
count = len(mc_file.readlines())
mc_file.close()

# initialize motion params mat
mc_params = np.full([count,6], np.nan)

# read in lines
mc_file = open(join(warpdir_out, 'mc', 'EPI_mcf.par'), 'r')
for i,line in enumerate(mc_file):
    this_line = line.strip()
    vals = [float(i) for i in line.split()]
    mc_params[i:] = vals

mc_file.close()

# plot motion
img_savedir = join(warpdir_out, 'mc_figures')
if not exists(img_savedir):
    makedirs(img_savedir)

# get motion params
rotx = mc_params[:,0]
roty = mc_params[:,1]
rotz = mc_params[:,2]
transx = mc_params[:,3]
transy = mc_params[:,4]
transz = mc_params[:,5]

fig=plt.figure(figsize=(18, 4), dpi= 80, facecolor='w', edgecolor='k')
_ = plt.plot(np.full([count,1],0), 'k--', linewidth=.5)
_ = plt.plot(rotx, 'b', label='rotx')
_ = plt.plot(roty, 'g', label='roty')
_ = plt.plot(rotz, 'r', label='rotz')
_ = plt.legend(fontsize=15)
_ = plt.ylabel('rotation in rads', fontsize=15)
_ = plt.xlabel('time in TRs', fontsize=15)
_ = plt.title('rotation during scan', fontsize=20)
fig.savefig(join(img_savedir, 'motion_rotation.png'))

fig=plt.figure(figsize=(18, 4), dpi= 80, facecolor='w', edgecolor='k')
_ = plt.plot(np.full([count,1],0), 'k--', linewidth=.5)
_ = plt.plot(transx, 'b', label='transx')
_ = plt.plot(transy, 'g', label='transy')
_ = plt.plot(transz, 'r', label='transz')
_ = plt.legend(fontsize=15)
_ = plt.ylabel('translation in mm', fontsize=15)
_ = plt.xlabel('time in TRs', fontsize=15)
_ = plt.title('translation during scan', fontsize=20)
fig.savefig(join(img_savedir, 'motion_translation.png'))


