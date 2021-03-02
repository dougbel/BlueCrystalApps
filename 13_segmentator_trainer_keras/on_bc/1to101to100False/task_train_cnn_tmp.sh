#!/bin/bash

#SBATCH --job-name=affseg
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=14
#SBATCH --gres=gpu:1
#SBATCH --time=1-16:00:00
#SBATCH --mem=64G
#SBATCH --mail-type=ALL


module load CUDA/8.0.44-GCC-5.4.0-2.26
module load libs/cudnn/5.1-cuda-8.0
module load languages/anaconda3/3.7

source activate keras_gpu
export PATH=$HOME/.conda/envs/keras_gpu/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/keras_segmentation:\$PYTHONPATH


srun python train_cnn_tmp.py --interaction laying_human_laying --architecture unet

srun python train_cnn_tmp.py --interaction reaching_out_low_human_reaching_out_low --architecture unet

srun python train_cnn_tmp.py --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture unet

srun python train_cnn_tmp.py --interaction sitting_human_sitting --architecture unet

srun python train_cnn_tmp.py --interaction standing_up_floor_human_standing_up --architecture unet