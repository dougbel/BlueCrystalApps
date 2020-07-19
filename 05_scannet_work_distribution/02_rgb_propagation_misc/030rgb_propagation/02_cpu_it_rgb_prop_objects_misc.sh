#!/bin/bash

#SBATCH --job-name=rgbobjn
#SBATCH --requeue
#SBATCH --partition=serial
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=2-12:00:00
#SBATCH --mem=32G
#SBATCH --mail-type=ALL
#SBATCH --array=0,7,13,16,17,19,20,21,22,23

module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate trimesh
export PATH=$HOME/.conda/envs/trimesh/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH

SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans
OUTPUT_DIR=/mnt/storage/scratch/csapo/ScanNet_parallel_analysis_misc
TRAINED_ITER_DIR=/mnt/storage/scratch/csapo/descriptors_repository
JSON_EXEC_FILE=/mnt/storage/home/csapo/projects/05_scannet_work_distribution/02_rgb_propagation_misc/02_objects_misc_testing.json

srun python rgb_prop.py --n_tasks 24 --dataset_scans_path $SCANS_DIR --output_path $OUTPUT_DIR --interactions_path $TRAINED_ITER_DIR --json_conf_execution_file $JSON_EXEC_FILE