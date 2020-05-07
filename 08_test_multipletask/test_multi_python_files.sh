#!/bin/bash

#SBATCH --job-name=mul_py
#SBATCH --partition=test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=14
#SBATCH --time=00:10:00
#SBATCH --mem=16G
#SBATCH --mail-type=ALL
#SBATCH --array=0-4

module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate trimesh
export PATH=$HOME/.conda/envs/trimesh/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH

SCANS_DIR=/mnt/storage/scratch/csapo/ScanNet/scans

srun python task1.py --dataset_scans_path $SCANS_DIR
srun python task2.py --dataset_scans_path $SCANS_DIR
srun python task3.py --dataset_scans_path $SCANS_DIR
srun python task4.py --dataset_scans_path $SCANS_DIR
#! TASK 3 has some intentional fails
#!    Conclusion:  On failing any of the step it run all other
#! TASK 1 has an intentional delay
#!    Conclusion: it RESPECT the step by step situation but not stop further step if one before fails