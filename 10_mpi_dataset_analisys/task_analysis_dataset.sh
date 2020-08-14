#!/bin/bash

#SBATCH --job-name=mpi_an
#SBATCH --partition=test
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=6
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --mem=16G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/home/csapo/scratch/conda_envs/mpi_trimesh
INPUT_DIR=/mnt/storage/home/csapo/scratch/npz_tmp

source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/mpi-master-slave:\$PYTHONPATH

srun --mpi=pmi2 python script_analysis_dataset.py --input_dir $INPUT_DIR