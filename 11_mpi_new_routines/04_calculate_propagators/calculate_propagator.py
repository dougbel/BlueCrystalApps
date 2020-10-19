import argparse

from mpi4py import MPI

from mpi_routines.master import MasterMultiRoutines
from mpi_routines.slaves.slave_calculate_propagator import SlaveCalculatePropagator

parser = argparse.ArgumentParser()
parser.add_argument('--work_directory', required=True, help='Path to work_directory folder')
parser.add_argument('--json_conf_execution_file', required=True, help='JSON file with execution parameters')
parser.add_argument('--test_result_directory', required=True, help='Path to test results in environment')
parser.add_argument('--conf_propagators_repository', required=True, help='Directory with propagators configurations')

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
                                  prefix_follow_up_column="calc_prop",
                                  json_conf_execution_file=opt.json_conf_execution_file)
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        SlaveCalculatePropagator(work_directory=opt.work_directory,
                                 test_result_directory=opt.test_result_directory,
                                 conf_propagators_repository=opt.conf_propagators_repository,
                                 json_conf_execution_file=opt.json_conf_execution_file).run()

    print('Task completed (rank %d)' % (rank))
