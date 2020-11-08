#!/bin/bash

#SBATCH --job-name=mpisteps
#SBATCH --partition=veryshort
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=14
#SBATCH --time=00:10:00
#SBATCH --mem=1G


module load OpenMPI/2.0.1-gcccuda-2016.10
module load languages/anaconda3/3.7

PREFIX_ENV=/mnt/storage/scratch/csapo/conda_envs/mpi_trimesh

source activate $PREFIX_ENV
export PATH=$PREFIX_ENV/bin:$PATH


echo "_________________________________________________________________________________"
echo "--------------------                FIRST RUN           ------------------------"
echo "_________________________________________________________________________________"
echo "RUNNING THE FIRST MPI  WAITING FOR 2 TASK EACH NODE, 4 IN TOTAL, 3 SLAVES 1 MASTER"

ARG_RUN=thisIsTheFIRSTrun
srun --mpi=pmi2 python hello_mpi_steps.py --argument $ARG_RUN



# echo "_________________________________________________________________________________"
# echo "--------------------                SECOND RUN           ------------------------"
# echo "_________________________________________________________________________________"
# echo "RUNNING THE SECOND MPI  WAITING FOR 2 TASK EACH NODE 4 IN TOTAL, 3 SLAVES 1 MASTER"
# echo "AND A DIFFERENT VARIABLE"

# ARG_RUn=thisIsTheSECONDrun
# srun --mpi=pmi2 python hello_mpi_steps.py --argument $ARG_RUN



echo "_________________________________________________________________________________"
echo "--------------------                SECOND RUN           ------------------------"
echo "_________________________________________________________________________________"
echo "RUNNING THE SECOND MPI  WAITING FOR 2 TASK EACH NODE 4 IN TOTAL, 3 SLAVES 1 MASTER"
echo "AND A DIFFERENT VARIABLE"

srun --mpi=pmi2 python hello_mpi_steps_2.py --argument thisIsTheSECONDrun



echo "_________________________________________________________________________________"
echo "--------------------                THIRD RUN           ------------------------"
echo "_________________________________________________________________________________"
echo "RUNNING THE FIRST MPI  WAITING FOR 2 TASK EACH NODE, 4 IN TOTAL, 3 SLAVES 1 MASTER"

ARG_RUN=thisIsTheFIRSTrun
srun --mpi=pmi2 python hello_mpi_steps.py --argument $ARG_RUN




echo "_________________________________________________________________________________"
echo "--------------------               FOURTH RUN           ------------------------"
echo "_________________________________________________________________________________"
echo "RUNNING THE FIRST MPI  WAITING FOR 2 TASK EACH NODE, 4 IN TOTAL, 3 SLAVES 1 MASTER"
echo "AND A DIFFERENT VARIABLE"

srun --mpi=pmi2 python hello_mpi_steps_2.py --argument thisIsTheFOURTHrun


