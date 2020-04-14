#!/bin/bash

#SBATCH --job-name=omp-test
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=28
#SBATCH --time=0:0:10
#SBATCH --mem=100M

# Load modules required for runtime e.g.
module load languages/intel/2017.01

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}
srun ./hello-omp
