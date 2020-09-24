#!/bin/bash

#SBATCH --job-name=mpi_fill
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00
#SBATCH --mem=32G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/train
SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans


source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:\$PYTHONPATH

srun --mpi=pmi2 python preprocessing_env.py --work_directory $WORKING_DIRECTORY --dataset_scans_path  $SCANS_DIR
