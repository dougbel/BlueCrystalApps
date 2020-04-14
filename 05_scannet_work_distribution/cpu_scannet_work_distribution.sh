#!/bin/bash

#SBATCH --job-name=2n7t2c
#SBATCH --partition=cpu
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=7
#SBATCH --cpus-per-task=2
#SBATCH --time=01:00:00
#SBATCH --mem=125G
#SBATCH --mail-type=ALL
#SBATCH --array=0-13%7
#!            #SBATCH --array=0-13%8  #will limit the number of simultaneously running tasks from this job array to 8
module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate trimesh
export PATH=$HOME/.conda/envs/trimesh/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH

python distribution.py --dataset_scans_path /mnt/storage/scratch/csapo/ScanNet/scans --output_path /mnt/storage/scratch/csapo/ScanNet_analysis_sitting --interactions_path /mnt/storage/scratch/csapo/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_500 --json_conf_execution_file /mnt/storage/home/csapo/projects/05_scannet_work_distribution/single_testing.json
