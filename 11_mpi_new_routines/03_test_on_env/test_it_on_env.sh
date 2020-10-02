#!/bin/bash

#SBATCH --job-name=envtest
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=3
#SBATCH --cpus-per-task=8
#SBATCH --time=20:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/train
SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans
TRAINED_ITER_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/descriptor_repository
JSON_EXEC_FILE=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/json_execution/single_testing_sitting.json


source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:\$PYTHONPATH

srun --mpi=pmi2 python test_it_on_env.py --work_directory $WORKING_DIRECTORY --dataset_scans_path  $SCANS_DIR --descriptors_repository $TRAINED_ITER_DIR --json_conf_execution_file $JSON_EXEC_FILE
