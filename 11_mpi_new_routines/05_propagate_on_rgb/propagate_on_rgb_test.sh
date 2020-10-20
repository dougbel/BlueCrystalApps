#!/bin/bash

#SBATCH --job-name=proprgbt
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=3
#SBATCH --cpus-per-task=8
#SBATCH --time=05:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH


SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans_test
WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/test
JSON_EXEC_FILE=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/json_execution/single_testing_sitting.json
PROPAGATORS_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/test/propagators

srun --mpi=pmi2 python propagate_on_rgb.py --dataset_scans_path  $SCANS_DIR --work_directory $WORKING_DIRECTORY --json_conf_execution_file $JSON_EXEC_FILE  --propagators_directory $PROPAGATORS_DIR
