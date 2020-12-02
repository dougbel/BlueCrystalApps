import argparse

from mpi4py import MPI

from mpi_routines.master import MasterAnalysisData
from mpi_routines.slaves.slave_analyser import SlaveAnalyser

parser = argparse.ArgumentParser()
parser.add_argument('--work_directory', required=True, help='Path to work_directory folder')
opt = parser.parse_args()
print(opt)

if __name__ == "__main__":

    name = MPI.Get_processor_name()
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()

    # activate it with debug purposes
    # import pydevd_pycharm
    # port_mapping = [35997, 33227, 45069]
    # pydevd_pycharm.settrace('localhost', port=port_mapping[rank], stdoutToServer=True, stderrToServer=True)
    # print(os.getpid())

    print('***************************************************************************')
    print('I am  %s rank %d (total %d)' % (name, rank, size))
    print('***************************************************************************')

    if rank == 0:  # Master

        app = MasterAnalysisData(slaves=range(1, size), working_dir=opt.work_directory)
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        SlaveAnalyser().run()

    print('Task completed (rank %d)' % rank)