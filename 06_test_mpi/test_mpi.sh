#!/bin/bash

#SBATCH --job-name=mpi4py_test
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=00:01:00
#SBATCH --mem=1G


module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

source activate mpi_trimesh_test

srun python hello_mpi.py