import argparse
import logging
import os
import socket

import numpy as np
import pandas as pd

from si.pipes.pipe import Pipe
from si.pipes.pipecalculatepropagator import PipeCalculatePropagator
from si.pipes.pipepropagateonimg import PipePropagateOnImg
from si.pipes.piperegistration import PipeRegistration
from si.pipes.pipesearchinvalidposes import PipeSearchInvalidPoses
from si.scannet.datascannet import DataScanNet

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_scans_path', required=True, help='Path to ScanNet dataset')


opt = parser.parse_args()
print(opt)

if __name__ == '__main__':
    n_nodes = int(os.getenv('SLURM_JOB_NUM_NODES'))
    n_tasks_per_node = int(os.getenv('SLURM_NTASKS_PER_NODE'))
    id_task = int(os.getenv('SLURM_ARRAY_TASK_ID'))
    n_tasks = int(os.getenv('SLURM_ARRAY_TASK_MAX')) + 1

    scannet_data = DataScanNet(opt.dataset_scans_path)
    size_scannet = len(scannet_data.scans)
    work_idxs = np.array_split(list(range(size_scannet)), n_tasks)[id_task]

    print('host_name        - '+ socket.gethostname())
    print('id_task          - '+ str(id_task))
    print('n_nodes          - '+ str(n_nodes))
    print('n_tasks_per_node - '+ str(n_tasks_per_node))
    print('n_tasks          - '+ str(n_tasks))
    print(opt.dataset_scans_path+ ' - Working section '+ str(id_task + 1)+ '/'+ str(n_tasks))
    print(str(work_idxs))

    print('DELAYING 1 minute Task 1')
    import time
    time.sleep(60)

    print('#########################################################################')
    print('###            TASK 1                                               #####')
    print('#########################################################################')