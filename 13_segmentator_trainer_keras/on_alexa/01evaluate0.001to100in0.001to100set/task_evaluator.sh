#!/bin/bash

export HDF5_USE_FILE_LOCKING='FALSE'

#conda activate keras_gpu
export PYTHONPATH=/home/hal/Abel/git_repositories/keras_segmentation:\$PYTHONPATH

echo  "child_laying_child_laying"
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction child_laying_child_laying --architecture segnet
CUDA_VISIBLE_DEVICES=0 srun python evaluator.py --interaction child_laying_child_laying --architecture unet
echo  "laying_human_laying"
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction laying_human_laying --architecture segnet
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction laying_human_laying --architecture unet
echo  "reaching_out_low_human_reaching_out_low"
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction reaching_out_low_human_reaching_out_low --architecture segnet
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction reaching_out_low_human_reaching_out_low --architecture unet
echo  "reaching_out_mid_low_human_reaching_out_mid_low"
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture segnet
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture unet
echo  "sitting_human_sitting"
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction sitting_human_sitting --architecture segnet
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction sitting_human_sitting --architecture unet
echo  "standing_up_floor_human_standing_up"
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction standing_up_floor_human_standing_up --architecture segnet
CUDA_VISIBLE_DEVICES=0 python evaluator.py --interaction standing_up_floor_human_standing_up --architecture unet
