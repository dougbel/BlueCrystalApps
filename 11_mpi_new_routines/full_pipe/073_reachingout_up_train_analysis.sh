#!/bin/bash

#SBATCH --job-name=rouptr
#SBATCH --partition=veryshort
#SBATCH --exclude=compute418
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=3
#SBATCH --exclusive
#SBATCH --time=2:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH

JSON_EXEC_FILE=/mnt/storage/scratch/csapo/analisys/mpi_routines/configs/json_execution/single_testing_reaching_out_up.json

SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans
TRAINED_ITER_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/configs/descriptor_repository
JSON_PROPAGATORS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/configs/json_propagators

WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/train
TEST_RESULTS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/train/env_test
PROPAGATORS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/train/propagators


echo "Analysis"
srun --mpi=pmi2 python ../06_data_analyser/analyze_data.py --work_directory $WORKING_DIRECTORY