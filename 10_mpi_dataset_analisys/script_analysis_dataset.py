import argparse
import itertools

from mpi4py import MPI
from mpi_master_slave import Master, Slave
from mpi_master_slave import WorkQueue
import pandas as pd
import numpy as np
from shutil import copyfile
import time
import os


class MyApp(object):
    """
    This is my application that has a lot of work to do so it gives work to do
    to its slaves until all the work is done
    """

    def __init__(self, slaves, input_path):
        # when creating the Master we tell it what slaves it can handle
        self.master = Master(slaves)
        # WorkQueue is a convenient class that run slaves on a tasks queue
        self.work_queue = WorkQueue(self.master)
        self.input_path = input_path

    def terminate_slaves(self):
        """
        Call this to make all slaves exit their run loop
        """
        self.master.terminate_slaves()

    def run(self):
        """
        This is the core of my application, keep starting slaves
        as long as there is work to do
        """
        #
        # let's prepare our work queue. This can be built at initialization time
        # but it can also be added later as more work become available
        #
        csv_follow_up = os.path.join(self.input_path, "follow_up_process.csv")
        pd_follow_up = pd.read_csv(csv_follow_up, index_col=0)
        l_scans = pd_follow_up.index.values.tolist()
        l_inter = [sub_path for sub_path in os.listdir(self.input_path)
                   if (not sub_path.endswith('_img_segmentation_w224_x_h224')
                       and os.path.isdir(os.path.join(self.input_path, sub_path)))]
        tuples_all = list(itertools.product(l_inter, l_scans))

        if os.path.isfile(os.path.join(os.getcwd(), 'file_name.csv')):
            df = pd.read_csv(os.path.join(os.getcwd(), 'file_name.csv'))
            tuples_ready = df.drop_duplicates(['interaction', 'scan'])[['interaction', 'scan']].values.tolist()
            l_task = [t for t in tuples_all if t not in tuples_ready]
        else:
            df = pd.DataFrame(columns=['interaction', 'scan', 'num_frame', 'n_t', 'n_p', 'n_n'])
            l_task = tuples_all

        data = [(self.input_path,) + data for data in l_task]

        for d in data:
            # 'data' will be passed to the slave and can be anything
            self.work_queue.add_work(data=d)

        #
        # Keeep starting slaves as long as there is work to do
        #
        while not self.work_queue.done():

            #
            # give more work to do to each idle slave (if any)
            #
            self.work_queue.do_work()

            #
            # reclaim returned data from completed slaves
            #
            for slave_return_data in self.work_queue.get_completed_work():
                done, partial_df,  message = slave_return_data
                if done:
                    print('Master: slave finished its task and says "%s"' % message)
                    df = df.append(partial_df, ignore_index=True)
                    if os.path.isfile(os.path.join(os.getcwd(), 'file_name.csv')):
                        copyfile(os.path.join(os.getcwd(), 'file_name.csv'),
                                 os.path.join(os.getcwd(), 'tmp_file_name.csv'))
                    df.to_csv(os.path.join(os.getcwd(), 'file_name.csv'))

            # sleep some time
            time.sleep(0.3)


class MySlave(Slave):
    """
    A slave process extends Slave class, overrides the 'do_work' method
    and calls 'Slave.run'. The Master will do the rest
    """

    def __init__(self):
        super(MySlave, self).__init__()
        self.threshold = 0.2

    def do_work(self, data):
        rank = MPI.COMM_WORLD.Get_rank()
        name = MPI.Get_processor_name()
        input_dir, interaction, scan = data
        data_dir = os.path.join(input_dir, interaction + '_img_segmentation_w224_x_h224', scan)
        print('  Slave %s rank %d EXECUTING it:"%s", scan: "%s"' % (name, rank, interaction, scan))
        data_compiled = np.load(os.path.join(data_dir, "scores_1.npz"))
        df = pd.DataFrame(columns=['interaction', 'scan', 'num_frame', 'n_t', 'n_p', 'n_n'])
        for key in data_compiled.keys():
            num_frame = int(key[12:12 + key[12:].find('_')])
            scores = data_compiled[key]
            n_t = scores.size
            n_p = len(np.where(scores > self.threshold)[0])
            n_n = n_t - n_p
            df = df.append(
                {'interaction': interaction, 'scan': scan, 'num_frame': num_frame, 'n_t': n_t, 'n_p': n_p, 'n_n': n_n},
                ignore_index=True)

        return True, df, '  Slave %s rank %d COMPLETED it:"%s", scan: "%s"' % (name, rank, interaction, scan)


parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', required=True, help='Input dir')
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

        app = MyApp(slaves=range(1, size), input_path=opt.input_dir)
        app.run()
        app.terminate_slaves()

    else:  # Any slave

        MySlave().run()

    print('Task completed (rank %d)' % (rank))
