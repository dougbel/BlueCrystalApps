#!/bin/bash

#SBATCH --job-name=callay
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=3
#SBATCH --cpus-per-task=8
#SBATCH --time=15:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH


JSON_EXEC_FILE=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/json_execution/single_testing_laying.json
TRAINED_ITER_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/descriptor_repository
JSON_PROPAGATORS_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/json_propagators


SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans
WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/train
TEST_RESULTS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/train/env_test
srun --mpi=pmi2 python ../03_test_on_env/test_it_on_env.py --work_directory $WORKING_DIRECTORY --dataset_scans_path  $SCANS_DIR --descriptors_repository $TRAINED_ITER_DIR --json_conf_execution_file $JSON_EXEC_FILE
srun --mpi=pmi2 python ../04_calculate_propagators/calculate_propagator.py --work_directory $WORKING_DIRECTORY --json_conf_execution_file $JSON_EXEC_FILE  --test_result_directory $TEST_RESULTS_DIR --conf_propagators_repository $JSON_PROPAGATORS_DIR


SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans_test
WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/test
TEST_RESULTS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines/test/env_test
srun --mpi=pmi2 python ../03_test_on_env/test_it_on_env.py --work_directory $WORKING_DIRECTORY --dataset_scans_path  $SCANS_DIR --descriptors_repository $TRAINED_ITER_DIR --json_conf_execution_file $JSON_EXEC_FILE
srun --mpi=pmi2 python ../04_calculate_propagators/calculate_propagator.py --work_directory $WORKING_DIRECTORY --json_conf_execution_file $JSON_EXEC_FILE  --test_result_directory $TEST_RESULTS_DIR --conf_propagators_repository $JSON_PROPAGATORS_DIR


