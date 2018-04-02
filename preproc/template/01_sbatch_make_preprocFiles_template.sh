#!/usr/bin/env bash

# Set current working directory
#SBATCH --workdir=.

# How long is job (in minutes)?
#SBATCH --time=30

# How much memory to allocate (in MB)?
#SBATCH --cpus-per-task=1 --mem=2000

# Name of jobs?
#SBATCH -J prep_unwarp

# Where to output log files?
#SBATCH -o '###SUB_DIR###/logs/prep-%A_%a.log'

# Number of jobs to run in parallel
#SBATCH --array=1

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
echo 'running prep warpfiles script...'
echo

CODE_DIR=###CODE_DIR###
python $CODE_DIR/01_make_preprocFiles.py

echo
echo '------------------------------'
