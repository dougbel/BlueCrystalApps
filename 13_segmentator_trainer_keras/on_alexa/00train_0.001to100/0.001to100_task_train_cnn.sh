#!/bin/bash

export HDF5_USE_FILE_LOCKING='FALSE'

#conda activate keras_gpu
export PYTHONPATH=/home/hal/Abel/git_repositories/keras_segmentation:\$PYTHONPATH

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction child_laying_child_laying --architecture segnet
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction child_laying_child_laying --architecture unet

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction laying_human_laying --architecture segnet
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction laying_human_laying --architecture unet

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction reaching_out_low_human_reaching_out_low --architecture segnet
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction reaching_out_low_human_reaching_out_low --architecture unet

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture segnet
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture unet

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction sitting_human_sitting --architecture segnet
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction sitting_human_sitting --architecture unet

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction standing_up_floor_human_standing_up --architecture segnet
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interaction standing_up_floor_human_standing_up --architecture unet
