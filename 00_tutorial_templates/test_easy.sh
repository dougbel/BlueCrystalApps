#!/bin/bash

#SBATCH --job-name=test_job
#SBATCH --partition=test
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=1
#SBATCH --time=0:0:10
#SBATCH --mem=100M

echo 'My first job'
srun hostname
