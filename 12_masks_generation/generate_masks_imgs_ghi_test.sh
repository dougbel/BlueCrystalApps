#!/bin/bash

#SBATCH --job-name=mask_gen
#SBATCH --partition=veryshort
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=3
#SBATCH --time=00:30:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo

SCANNET_ANALYSIS_DIR=/mnt/storage/scratch/csapo/analisys/mpi_routines
STAGE=test
INTERACTIONS_SET=good_human_inter
ANALYSIS_INTERSECTIONS_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/analysis
OUTPUT_DIR=/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn
ANALYSIS_INTERSECTION_PERCENTAGES=1to100

source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:.:\$PYTHONPATH

srun --mpi=pmi2 python generate_masks_imgs.py --scannet_analysis_dir $SCANNET_ANALYSIS_DIR --stage $STAGE --interactions_set $INTERACTIONS_SET --analysis_intersections_dir $ANALYSIS_INTERSECTIONS_DIR --output_dir $OUTPUT_DIR --analysis_intersection_percentages $ANALYSIS_INTERSECTION_PERCENTAGES


