#!/usr/bin/env python3

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

