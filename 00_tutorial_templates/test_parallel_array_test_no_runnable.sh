#!/bin/bash

#SBATCH --job-name=test_job
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=0:0:10
#SBATCH --mem=100M
#SBATCH --array=100-149

srun my-analysis-program --temperature=$SLURM_ARRAY_TASK_ID
