import argparse

from mpi4py import MPI

from mpi_routines.master import MasterMultiRoutines
from mpi_routines.slaves.slave_propagate_on_frames import SlavePropagateOnFrames

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_scans_path', required=True, help='Path to ScanNet dataset')
parser.add_argument('--work_directory', required=True, help='Path to work_directory folder')
parser.add_argument('--json_conf_execution_file', required=True, help='JSON file with execution parameters')
parser.add_argument('--propagators_directory', required=True, help='Directory with propagators calculated')

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
        app = MasterMultiRoutines(slaves=range(1, size),
                                  work_directory=opt.work_directory,
                                  prefix_follow_up_column="frame_prop",
                                  json_conf_execution_file=opt.json_conf_execution_file)
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        SlavePropagateOnFrames(dataset_scans_path=opt.dataset_scans_path,
                               work_directory=opt.work_directory,
                               propagators_directory=opt.propagators_directory,
                               json_conf_execution_file=opt.json_conf_execution_file).run()

    print('Task completed (rank %d)' % (rank))
