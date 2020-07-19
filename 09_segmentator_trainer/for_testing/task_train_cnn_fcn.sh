#!/bin/bash

#SBATCH --job-name=fcn8_tmp
#SBATCH --partition=gpu_veryshort
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=0:59:00
#SBATCH --mem=32G
#SBATCH --mail-type=ALL


module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate keras_gpu
export PATH=$HOME/.conda/envs/keras_gpu/bin:$PATH

srun python train_cnn_fcn.py