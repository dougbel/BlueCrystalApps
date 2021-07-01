#!/bin/bash

#SBATCH --job-name=sdf_gen
#SBATCH --partition veryshort
#SBATCH --nodes=15
#SBATCH --ntasks-per-node=3
#SBATCH --cpus-per-task=8
#SBATCH --time=6:00:00
#SBATCH --mem=96G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
SCANS_DIR=/mnt/storage/home/csapo/scratch/PLACE_comparisson/datasets/replica_v1/scenes_downsampled


source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:.:\$PYTHONPATH

echo "working on apartment_1"
srun --mpi=pmi2 python 02_sdf_calculation_following_prox.py --dataset_dir $SCANS_DIR  --scene apartment_1
echo "working on frl_apartment_0"
srun --mpi=pmi2 python 02_sdf_calculation_following_prox.py --dataset_dir $SCANS_DIR  --scene frl_apartment_0
echo "working on hotel_0"
srun --mpi=pmi2 python 02_sdf_calculation_following_prox.py --dataset_dir $SCANS_DIR  --scene hotel_0
echo "working on office_2"
srun --mpi=pmi2 python 02_sdf_calculation_following_prox.py --dataset_dir $SCANS_DIR  --scene office_2
echo "working on room_0"
srun --mpi=pmi2 python 02_sdf_calculation_following_prox.py --dataset_dir $SCANS_DIR  --scene room_0

