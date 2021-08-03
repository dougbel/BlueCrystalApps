#!/bin/bash

#SBATCH --job-name=envtest
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=12
#SBATCH --time=16:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
WORKING_DIRECTORY=/mnt/storage/home/csapo/scratch/PLACE_trainings/test
SCANS_DIR=/mnt/storage/home/csapo/scratch/PLACE_trainings/datasets
CONFIG_DIR=/mnt/storage/home/csapo/scratch/PLACE_trainings/config


source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:.:\$PYTHONPATH

srun --mpi=pmi2 python 01_testing.py --dataset_scans_path $SCANS_DIR --work_directory $WORKING_DIRECTORY  --config_directory $CONFIG_DIR
