#!/bin/bash
#SBATCH --account=cosc012641
#SBATCH --job-name=sdf_gen
#SBATCH --partition=hmem
  #! #SBATCH --partition=cpu
  #! SBATCH --partition test
  #! #SBATCH --nodes=12
#SBATCH --nodes=4
    #! SBATCH --nodes=2
#SBATCH --ntasks-per-node=3
#SBATCH --cpus-per-task=8
    #! #SBATCH --time=13-23:59:00
    #! SBATCH --time=1:00:00
#SBATCH --time=13-23:59:00
    #! SBATCH --mem=100G
#SBATCH --mem=300G
#SBATCH --mail-type=ALL

module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/trimesh_vedo
GRID_DIM=384


source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH
export PYTHONPATH=/mnt/storage/home/csapo/git_repositories/iTpy:/mnt/storage/home/csapo/git_repositories/iTpyClearance:/mnt/storage/home/csapo/git_repositories/mpi-master-slave:/mnt/storage/home/csapo/git_repositories/mpi_routines:.:\$PYTHONPATH


#PROX_SCANS_DIR=/user/home/csapo/work/Lander/dataset/mp3d/scene
#PROX_OUTPUT_DIR=/user/home/csapo/work/Lander/dataset/mp3d/scene/sdf_384

echo 'working on 17DRP5sb8fy-bedroom'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene 17DRP5sb8fy-bedroom --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384
echo 'working on 17DRP5sb8fy-familyroomlounge'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene 17DRP5sb8fy-familyroomlounge --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384
echo 'working on 17DRP5sb8fy-livingroom'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene 17DRP5sb8fy-livingroom --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384
echo 'working on sKLMLpTHeUy-familyname_0_1'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene sKLMLpTHeUy-familyname_0_1 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384
echo 'working on X7HyMhZNoso-livingroom_0_16'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene X7HyMhZNoso-livingroom_0_16 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384
echo 'working on zsNo4HB9uLZ-bedroom0_0'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene zsNo4HB9uLZ-bedroom0_0 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384
echo 'working on zsNo4HB9uLZ-livingroom0_13'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes  --scene zsNo4HB9uLZ-livingroom0_13 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/mp3d/scenes/sdf_384


echo 'working on apartment_1'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes  --scene apartment_1 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes/sdf_384
echo 'working on frl_apartment_0'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes  --scene frl_apartment_0 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes/sdf_384
echo 'working on hotel_0'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes  --scene hotel_0 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes/sdf_384
echo 'working on office_2'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes  --scene office_2 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes/sdf_384
echo 'working on room_0'
srun --mpi=pmi2 python PROX_sdf_calculation_following_prox_MPI.py --scans_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes  --scene room_0 --grid_dim $GRID_DIM --output_dir /user/home/csapo/work/Lander/dataset/replica_v1/scenes/sdf_384
