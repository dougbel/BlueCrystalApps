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
# data paths
parser.add_argument('--dataset_scans_path', required=True, help='Path to ScanNet dataset')
parser.add_argument('--output_path', required=True, help='Path to output folder')
# parser.add_argument('--interactions_path', required=True, help='Interactions path to test in environment')
# parser.add_argument('--json_conf_execution_file', required=True, help='JSON file with execution parameters')

opt = parser.parse_args()
print(opt)

if __name__ == '__main__':
    n_nodes = int(os.getenv('SLURM_JOB_NUM_NODES'))
    n_tasks_per_node = int(os.getenv('SLURM_NTASKS_PER_NODE'))
    id_task = int(os.getenv('SLURM_ARRAY_TASK_ID'))
    n_tasks = int(os.getenv('SLURM_ARRAY_TASK_MAX')) + 1


    output_path = os.path.join(opt.output_path, "task_" + str(id_task))
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    logging_file = os.path.join(output_path, 'scannet_process.log')
    logging.basicConfig(filename=logging_file, filemode='a', level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    # Creating multiple scenes produces some harmless error messages, to AVOID
    logging.getLogger('pyembree').disabled = True

    scannet_data = DataScanNet(opt.dataset_scans_path)
    size_scannet = len(scannet_data.scans)
    work_idxs = np.array_split(list(range(size_scannet)), n_tasks)[id_task]
    scannet_data.scans = [scannet_data.scans[i] for i in work_idxs]
    scannet_data.sens_files = [scannet_data.sens_files[i] for i in work_idxs]
    scannet_data.env_files = [scannet_data.env_files[i] for i in work_idxs]

    logging.info('host_name        - '+ socket.gethostname())
    logging.info('id_task          - '+ str(id_task))
    logging.info('n_nodes          - '+ str(n_nodes))
    logging.info('n_tasks_per_node - '+ str(n_tasks_per_node))
    logging.info('n_tasks          - '+ str(n_tasks))
    logging.info(opt.dataset_scans_path+ ' - Working section '+ str(id_task + 1)+ '/'+ str(n_tasks))
    logging.info(str(work_idxs))

    follow_up_file = os.path.join(output_path, Pipe.follow_up_file_name)
    if not os.path.isfile(follow_up_file):
        follow_up_data = pd.DataFrame(index=scannet_data.scans)
    else:
        follow_up_data = pd.read_csv(follow_up_file, index_col=0)

    ##### -------------------------------------------------------------------------------------------------- #######
    p_registration = PipeRegistration(follow_up_data, scannet_data)
    p_registration.process(output_path)
    #
    # ##### -------------------------------------------------------------------------------------------------- #######
    #p_search_invalid_Poses = PipeSearchInvalidPoses(follow_up_data, scannet_data)
    #p_search_invalid_Poses.process(output_path)
    #
    # ##### -------------------------------------------------------------------------------------------------- #######
    # p_test_propagate = PipeCalculatePropagator(follow_up_data, scannet_data, opt.interactions_path,
    #                                            opt.json_conf_execution_file)
    # p_test_propagate.process(output_path)
    #
    # p_test_propagate = PipeCalculatePropagator_Restricted(follow_up_data, scannet_data, opt.interactions_path, opt.json_conf_execution_file)
    # p_test_propagate.process(output_path)
    #
    # ##### -------------------------------------------------------------------------------------------------- #######
    # p_test_propagator = TestPipePropagation(follow_up_data, scannet_data, opt.json_conf_execution_file)
    # p_test_propagator.process(output_path)

    # p_propagator_img = PipePropagateOnImg(follow_up_data, scannet_data, opt.json_conf_execution_file, mask_width=224,
    #                                       mask_height=224, stride=100, visualize=False)
    # p_propagator_img.process(output_path)
