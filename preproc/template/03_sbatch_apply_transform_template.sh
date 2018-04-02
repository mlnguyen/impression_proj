#!/usr/bin/env bash

# Set current working directory
#SBATCH --workdir=.

# How long is job (in minutes)?
#SBATCH --time=20

# How much memory to allocate (in MB)?
#SBATCH --cpus-per-task=1 --mem=2000

# Name of jobs?
#SBATCH -J xform

# Where to output log files?
#SBATCH -o '###SUB_DIR###/logs/xform-%A_%a.log'

# Number of jobs to run in parallel
#SBATCH --array=1-###N_RUNS###

# load modules
# set up modules
echo '------------------------------'
echo "module setup"
. /usr/share/Modules/init/bash
module purge
module load fsl
module load pyger
module list
echo

# Print job info
echo '------------------------------'
echo "job info"

echo "slurm job id: " $SLURM_JOB_ID
echo "slurm array task id: " $SLURM_ARRAY_TASK_ID
echo "subject id: " ###SUB_ID###
echo

# Run
echo '------------------------------'
echo 'running preproc: applying transform to standard space ...'
echo

CODE_DIR=###CODE_DIR###
python $CODE_DIR/03_apply_transform.py $SLURM_ARRAY_TASK_ID

echo
echo '------------------------------'
