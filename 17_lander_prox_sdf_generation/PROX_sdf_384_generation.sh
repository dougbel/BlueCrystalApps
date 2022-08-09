#!/bin/bash

#SBATCH --job-name=sdf_gen
#SBATCH --partition=cpu
    #! SBATCH --partition test
#SBATCH --nodes=16
    #! SBATCH --nodes=2
#SBATCH --ntasks-per-node=6
#SBATCH --cpus-per-task=4

#SBATCH --time=3-23:59:00
    #! SBATCH --time=1:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
GRID_DIM=384


source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:.:\$PYTHONPATH


PROX_SCANS_DIR=/user/home/csapo/work/Lander/dataset/prox/scene_artefact_removed
PROX_OUTPUT_DIR=/user/home/csapo/work/Lander/dataset/prox/scene_artefact_removed/sdf_384

echo "working on BasementSittingBooth"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene BasementSittingBooth --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on MPH11"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene MPH11 --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on MPH112"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene MPH112 --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on MPH16"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene MPH16 --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on MPH1Library"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene MPH1Library --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on MPH8"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene MPH8 --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on N0SittingBooth"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene N0SittingBooth --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on N0Sofa"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene N0Sofa --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on N3Library"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene N3Library --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on N3Office"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene N3Office --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on N3OpenArea"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene N3OpenArea --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
echo "working on Werkraum"
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir $PROX_SCANS_DIR  --scene Werkraum --grid_dim $GRID_DIM --output_dir $PROX_OUTPUT_DIR
