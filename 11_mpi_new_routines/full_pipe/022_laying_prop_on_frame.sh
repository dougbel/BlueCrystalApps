#!/bin/bash

#SBATCH --job-name=proplay
#SBATCH --exclude=compute418
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=14
#SBATCH --time=1-12:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:/mnt/storage/home/csapo/git_repositories/si:/mnt/storage/home/csapo/git_repositories/mpi_routines:\$PYTHONPATH

JSON_EXEC_FILE=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/configs/json_execution/single_testing_laying.json

WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/train
SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans
PROPAGATORS_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train/propagators
srun --mpi=pmi2 python ../05_propagate_on_frame/propagate_on_frames.py --dataset_scans_path  $SCANS_DIR --work_directory $WORKING_DIRECTORY --json_conf_execution_file $JSON_EXEC_FILE  --propagators_directory $PROPAGATORS_DIR


WORKING_DIRECTORY=/mnt/storage/scratch/csapo/analisys/mpi_routines/test
SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans_test
PROPAGATORS_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/test/propagators
srun --mpi=pmi2 python ../05_propagate_on_frame/propagate_on_frames.py --dataset_scans_path  $SCANS_DIR --work_directory $WORKING_DIRECTORY --json_conf_execution_file $JSON_EXEC_FILE  --propagators_directory $PROPAGATORS_DIR
