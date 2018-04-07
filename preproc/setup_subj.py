#!/usr/bin/env python3

from os.path import isfile, join, exists
from os import listdir, makedirs, walk, remove, getlogin
import pandas as pd
import re
import numpy as np
import fileinput
import subprocess

#---- Set subject specific variables ----#
# Set subject ID
subid = 'impr_g2_s02_030818'

# manually set scan num, type, conds
anat_num = [3]
fieldmap_nums = [8,9]
pos_epi_num = [5]
neg_epi_num = [4]
mix_epi_num = [6]
pie_epi_num = [7]

ref_scan = 'pieman'
scan_conds = ['pos2', 'neg2', 'mixed2', 'pieman']
print('\n\nsetting up ' + subid + '...\n')

#---- Set experiment-specific parameters ----#
# Set projdir
projdir = '/mnt/bucket/labs/hasson/mai/projects/impressions'
refbrain = '/jukebox/pkgs/FSL/5.0.9/data/standard/MNI152_T1_2mm_brain'

# Set data dir
datadir = join(projdir, 'data')

# Set code dir
codedir = join(projdir, 'code', 'preproc', 'bash')

# Set template dir
templatedir = join(projdir, 'code', 'preproc', 'template')

# Set niftidir
niftidir = join(datadir, subid, 'raw', 'nii')

# Set outputdir
anat_outdir = join(datadir, subid, 'data', 'niftis')
if not exists(anat_outdir):
    print(anat_outdir + ' does not exist, creating')
    makedirs(anat_outdir)

# Set subject script dir
preproc_script_dir = join(datadir, subid, 'preproc', 'scripts')
if not exists(preproc_script_dir):
    print(preproc_script_dir + ' does not exist, creating')
    makedirs(preproc_script_dir)    


#---- Copy and modify preproc scripts for subject ----#
# Setup script: 01_make_preprocFiles.py
template_script = join(templatedir, '01_make_preprocFiles_template.py')
subj_script = join(preproc_script_dir, '01_make_preprocFiles.py')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_ID###', "'" + subid + "'", line.rstrip())
    line = re.sub('###PROJ_DIR###', "'" + projdir + "'", line.rstrip())
    line = re.sub('###REF_SCAN###', "'" + ref_scan + "'", line.rstrip())
    print(line)
fileinput.close()

# Setup script: 01_sbatch_make_preprocFiles.sh
template_script = join(templatedir, '01_sbatch_make_preprocFiles_template.sh')
subj_script = join(preproc_script_dir, '01_sbatch_make_preprocFiles.sh')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_DIR###', join(datadir,subid), line.rstrip())
    line = re.sub('###SUB_ID###', subid, line.rstrip())
    line = re.sub('###CODE_DIR###', "'" + preproc_script_dir + "'", line.rstrip())
    print(line)
fileinput.close()


# Setup script: 02_run_preproc.py
template_script = join(templatedir, '02_run_preproc_template.py')
subj_script = join(preproc_script_dir, '02_run_preproc.py')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_ID###', "'" + subid + "'", line.rstrip())
    line = re.sub('###CONDS###', str(scan_conds), line.rstrip())
    line = re.sub('###PROJ_DIR###', "'" + projdir + "'", line.rstrip())
    print(line)
fileinput.close()

# Setup script: 02_sbatch_run_preprpoc.py
template_script = join(templatedir, '02_sbatch_run_preproc_template.sh')
subj_script = join(preproc_script_dir, '02_sbatch_run_preproc.sh')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_DIR###', join(datadir,subid), line.rstrip())
    line = re.sub('###CODE_DIR###', "'" + preproc_script_dir + "'", line.rstrip())
    line = re.sub('###SUB_ID###', subid, line.rstrip())
    line = re.sub('###N_RUNS###', str(len(scan_conds)) , line.rstrip())
    print(line)
fileinput.close()

# setup script: 03_apply_transform.py
template_script = join(templatedir, '03_apply_transform_template.py')
subj_script = join(preproc_script_dir, '03_apply_transform.py')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_ID###', "'" + subid + "'", line.rstrip())
    line = re.sub('###SUB_DIR###', "'" + join(datadir,subid) + "'", line.rstrip())
    line = re.sub('###CODE_DIR###', "'" + codedir + "'", line.rstrip())
    line = re.sub('###REF_BRAIN###', "'" + refbrain + "'", line.rstrip())
    print(line)
fileinput.close()

# Setup script: 03_sbatch_apply_transform.sh
template_script = join(templatedir, '03_sbatch_apply_transform_template.sh')
subj_script = join(preproc_script_dir, '03_sbatch_apply_transform.sh')
output = subprocess.check_output(['cp', template_script, subj_script])

for line in fileinput.input(subj_script, inplace=1):
    line = re.sub('###SUB_DIR###', join(datadir,subid), line.rstrip())
    line = re.sub('###CODE_DIR###', preproc_script_dir, line.rstrip())
    line = re.sub('###SUB_ID###', subid, line.rstrip())
    line = re.sub('###N_RUNS###', str(len(scan_conds)) , line.rstrip())
    print(line)


#---- Save scan info -----#
# organize scan info
anat = pd.DataFrame({'preprocDir': [0], 'scanNum': anat_num, 'scanType': 'anat', 'scanCond':'0'}, index=['anat'])

fieldmaps = pd.DataFrame({'preprocDir': [0,0], 'scanNum': fieldmap_nums, 'scanType': ['fieldmap', 'fieldmap'],
			'scanCond': ['0', '0']}, index=['se_fieldmap_ap', 'se_fieldmap_pa'])

pos_epi = pd.DataFrame({'preprocDir': 'run1', 'scanNum': pos_epi_num, 'scanType': 'epi', 'scanCond': [scan_conds[0]]}, index=[scan_conds[0]])
neg_epi = pd.DataFrame({'preprocDir': 'run2', 'scanNum': neg_epi_num, 'scanType': 'epi', 'scanCond': [scan_conds[1]]}, index=[scan_conds[1]])
mix_epi = pd.DataFrame({'preprocDir': 'run3', 'scanNum': mix_epi_num, 'scanType': 'epi', 'scanCond': [scan_conds[2]]}, index=[scan_conds[2]])
pie_epi = pd.DataFrame({'preprocDir': 'run4', 'scanNum': pie_epi_num, 'scanType': 'epi', 'scanCond': [scan_conds[3]]}, index=[scan_conds[3]])

df = pd.concat([pos_epi, neg_epi, mix_epi, pie_epi, fieldmaps, anat])

# automatically get scan names
niftiNames = np.array([])
niftis_all = listdir(niftidir)

for ind,row in df.iterrows():
    scanNum = row['scanNum']
    for filename in niftis_all:
        if str(scanNum) + '_' in filename:
            niftiNames = np.append(niftiNames, filename)
            break

# add nifti names to dataframe
df['niftiName'] = niftiNames

# add anatomies to scan info
newNiftis = pd.DataFrame({'niftiName': [subid + '_t1w_reorient.nii.gz', subid + '_t1w_reorient_brain.nii.gz'],
                          'scanNum': [0,0], 'scanType': ['anat', 'anat'], 'scanCond': ['0', '0'],
                          'preprocDir': [0,0]}, index=['anat_reorient', 'anat_brain'] )

# Save scan info
df = df.append(newNiftis)
df.to_csv(join(datadir, subid, 'scanInfo.csv'))

print(df)
print('\n**** done!\n')


# # ---- Reorient and extract brain ----------------------------------------------
anat_orig = join(niftidir, df.loc['anat']['niftiName'])
anat_reorient = join(anat_outdir, subid + '_t1w_reorient.nii.gz')
output = subprocess.check_output([join(codedir, 'prep_anat.sh'), anat_orig, anat_reorient, anat_outdir])




