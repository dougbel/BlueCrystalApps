#!/bin/bash

#SBATCH --job-name=mpi-test
#SBATCH --partition=test
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=28
#SBATCH --cpus-per-task=1
#SBATCH --time=0:0:10
#SBATCH --mem-per-cpu=100M

# Load modules required for runtime e.g.
module load languages/intel/2017.01

export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
srun ./hello-mpi
