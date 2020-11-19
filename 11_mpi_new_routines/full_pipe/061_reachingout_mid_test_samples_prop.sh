#!/bin/bash

#SBATCH --job-name=romte
#SBATCH --partition=veryshort
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=14
#SBATCH --exclusive
#SBATCH --time=5:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH

JSON_EXEC_FILE=/mnt/storage/scratch/csapo/analisys/mpi_routines/configs/json_execution/multiple_reaching_out_mid.json

SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans_test
TRAINED_ITER_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/configs/descriptor_repository
JSON_PROPAGATORS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/configs/json_propagators

WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/test
TEST_RESULTS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/test/env_test
PROPAGATORS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/test/propagators

srun --mpi=pmi2 python ../04_propagate_on_samples/propagate_on_samples.py --work_directory $WORKING_DIRECTORY --json_conf_execution_file $JSON_EXEC_FILE