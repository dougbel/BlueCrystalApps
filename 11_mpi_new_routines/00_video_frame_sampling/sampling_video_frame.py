import argparse

from mpi4py import MPI

from mpi_routines.master import MasterRoutines
from mpi_routines.slaves.slave_sampler_video import SlaveSamplerVideo

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_scans_path', required=True, help='Path to ScanNet dataset')
parser.add_argument('--work_directory', required=True, help='Path to work_directory folder')
parser.add_argument('--stride', required=True, help='Get frame every?')
parser.add_argument('--width', required=True, help='Width of sampling image')
parser.add_argument('--height', required=True, help='Height of sampling image')

opt = parser.parse_args()
print(opt)

if __name__ == "__main__":

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    # activate it with debug purposes
    # import pydevd_pycharm
    # port_mapping = [40311, 41361, 37937]
    # pydevd_pycharm.settrace('localhost', port=port_mapping[rank], stdoutToServer=True, stderrToServer=True)
    # print(os.getpid())

    print('***************************************************************************')
    print('I am  %s rank %d (total %d)' % (name, rank, size))
    print('***************************************************************************')

    if rank == 0:  # Master
        follow_up_column = "frame_img_samplings_w" + opt.width + "h" + opt.height + "s" + opt.stride

        app = MasterRoutines(slaves=range(1, size), work_directory=opt.work_directory, follow_up_column=follow_up_column)
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        SlaveSamplerVideo(dataset_scans_path=opt.dataset_scans_path, work_directory=opt.work_directory,
                          stride=int(opt.stride), width=int(opt.width), height=int(opt.height)).run()

        print('Task completed (rank %d)' % (rank))
