README.txt

1. Convert dicoms to niftis: navigate to project code directory
   a. Open convert_dcm2nii.sh in text editor
   b. Change subject id to current subject. Save and close
   c. run: ./convert_dcm2nii.sh

2. Setup subject
   a. Open setup_subj.py in project code directory
   b. Change subject id and run nums for this run. Save and close
   c. run: module load pyger; python ./setup_subj.py

3. Run brain extraction. Step (2) will automatically launch fslview and Bet. 
Use FSLview to roughly locate center of brain. Run Bet using intensity = .35, 
robust brain centre estimation, and the center coordinates. Check result in 
fslview. 
    NB: you can automatically run Bet without looking at the GUI. I highly
    discourage automatic brain extraction as it isn't reliable brain to brain

4. Prepare preproc files: make fieldmaps for B0 correct (blip up/down method), 
extract ref vols for motion correction. Outputs fieldmap images to check 
unwarping of fieldmaps. Runtime: ~15 min
   a. Navigate to subject directory
   b. Run: sbatch preproc/scripts/01_sbatch_make_preprocFiles.sh

5. Run preprocessing: uses files from part (4) to do fieldmap correction and
motion correction using FSL's applyunwarp. Then runs feat to do standard 
preprocessing (align to standard, high-pass filtering, spatial smoothing 
[FWHM = 4 mm]. Outputs figures showing fieldmap correction, motion estimates,
feat results.
   a. Run: sbatch preproc/scripts/02_sbatch_run_preproc.sh

6. Apply transform: transform processed niftis from subject space to MNI
standard space.
   a. Run: sbatch preproc/scripts/03_sbatch_apply_transform.sh







