#!/bin/bash

export HDF5_USE_FILE_LOCKING='FALSE'

#conda activate keras_gpu
export PYTHONPATH=/media/alexa/DATA/Abel/git_repositories/keras_segmentation:\$PYTHONPATH


INTERACTIONS_SET=good_human_inter
ANALYSIS_INTERSECTION_PERCENTAGES=0.001to100
IGNORE_BACKGROUNG=True

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction child_laying_child_laying --architecture segnet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction child_laying_child_laying --architecture unet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction laying_human_laying --architecture segnet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction laying_human_laying --architecture unet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction reaching_out_low_human_reaching_out_low --architecture segnet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction reaching_out_low_human_reaching_out_low --architecture unet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture segnet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction reaching_out_mid_low_human_reaching_out_mid_low --architecture unet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction sitting_human_sitting --architecture segnet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction sitting_human_sitting --architecture unet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG

CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction standing_up_floor_human_standing_up --architecture segnet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
CUDA_VISIBLE_DEVICES=0 python train_cnn.py --interactions_set $INTERACTIONS_SET --interaction standing_up_floor_human_standing_up --architecture unet --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES --ignore_background $IGNORE_BACKGROUNG
