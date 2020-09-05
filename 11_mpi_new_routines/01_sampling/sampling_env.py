import argparse

from mpi4py import MPI

from mpi_routines.master import MasterSampler
from mpi_routines.slaves.slave_sampler import SlaveSampler

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_scans_path', required=True, help='Path to ScanNet dataset')
parser.add_argument('--work_directory', required=True, help='Path to work_directory folder')
opt = parser.parse_args()
print(opt)

if __name__ == "__main__":

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    print('***************************************************************************')
    print('I am  %s rank %d (total %d)' % (name, rank, size))
    print('***************************************************************************')

    if rank == 0:  # Master

        app = MasterSampler(slaves=range(1, size), work_directory=opt.work_directory, follow_up_column="env_sampled")
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        SlaveSampler(dataset_scans_path=opt.dataset_scans_path, work_directory=opt.work_directory).run()

    print('Task completed (rank %d)' % (rank))
