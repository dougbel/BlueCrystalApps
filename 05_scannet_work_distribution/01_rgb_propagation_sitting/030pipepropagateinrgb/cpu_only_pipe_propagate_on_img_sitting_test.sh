#!/bin/bash

#SBATCH --job-name=sitting_rgb
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=14
#SBATCH --time=04:00:00
#SBATCH --mem=32G
#SBATCH --mail-type=ALL
#SBATCH --array=0-23
#!            #SBATCH --array=0-13%8  #will limit the number of simultaneously running tasks from this job array to 8
module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate trimesh
export PATH=$HOME/.conda/envs/trimesh/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH

srun python only_pipe_propagate_on_img.py --dataset_scans_path /mnt/storage/scratch/csapo/ScanNet/scans_test --output_path /mnt/storage/scratch/csapo/ScanNet_parallel_analysis_test --interactions_path /mnt/storage/scratch/csapo/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_500 --json_conf_execution_file /mnt/storage/home/csapo/projects/05_scannet_work_distribution/01_rgb_propagation_sitting/sitting_testing.json
