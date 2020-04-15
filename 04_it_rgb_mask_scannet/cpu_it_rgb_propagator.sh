#!/bin/bash

#SBATCH --job-name=it_rgb_propagator
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=14
#SBATCH --cpus-per-task=1
#SBATCH --time=5:00:00
#SBATCH --mem=32G
#SBATCH --mail-type=FAIL


module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate trimesh
export PATH=$HOME/.conda/envs/trimesh/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH



srun python 11_pipeline_extraction.py --dataset_scans_path /mnt/storage/scratch/csapo/ScanNet_small/scans --output_path /mnt/storage/scratch/csapo/ScanNet_small_analysis --interactions_path /mnt/storage/home/csapo/projects/it_rgb_mask_scannet/data/descriptors_repository/IBSMesh_400_4_OnGivenPointCloudWeightedSampler_5_500 --json_conf_execution_file /mnt/storage/home/csapo/projects/it_rgb_mask_scannet/data/single_testing.json
