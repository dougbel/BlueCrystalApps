#!/bin/bash

#SBATCH --job-name=Pnpy_npz
#SBATCH --requeue
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=14
#SBATCH --time=20:00:00
#SBATCH --mem=32G
#SBATCH --mail-type=ALL
#SBATCH --array=0-23

module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate trimesh
export PATH=$HOME/.conda/envs/trimesh/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/si:\$PYTHONPATH


srun python PARALLEL_from_npy_to_npz_parallel.py --src_path /mnt/storage/home/csapo/scratch/ScanNet_parallel_analysis_misc
