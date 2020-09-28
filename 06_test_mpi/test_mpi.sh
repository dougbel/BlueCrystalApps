#!/bin/bash

#SBATCH --job-name=mpi4py_test
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=2
#SBATCH --time=00:01:00
#SBATCH --mem=1G


module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/mpi_trimesh

source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH

srun --mpi=pmi2 python hello_mpi.py