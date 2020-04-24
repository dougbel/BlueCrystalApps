import argparse
import logging
import os

import pandas as pd

from si.pipes.pipe import Pipe
from si.pipes.pipecalculatepropagator import PipeCalculatePropagator
from si.pipes.piperegistration import PipeRegistration
from si.pipes.pipesearchinvalidposes import PipeSearchInvalidPoses
from si.scannet.datascannet import DataScanNet
from si.pipes.pipepropagateonimg import PipePropagateOnImg

parser = argparse.ArgumentParser()
# data paths
parser.add_argument('--dataset_scans_path', required=True, help='Path to ScanNet dataset')
parser.add_argument('--output_path', required=True, help='Path to output folder')
parser.add_argument('--interactions_path', required=True, help='Interactions path to test in environment')
parser.add_argument('--json_conf_execution_file', required=True, help='JSON file with execution parameters')
# parser.add_argument('--follow_up_file', default='', required=False, help='File with the follow up information')

opt = parser.parse_args()
print(opt)




if __name__ == '__main__':
    if not os.path.exists(opt.output_path):
        os.makedirs(opt.output_path)

    logging_file = os.path.join(opt.output_path, 'scannet_process.log')
    logging.basicConfig(filename=logging_file, filemode='a', level=logging.INFO,
                         format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    # Creating multiple scenes produces some harmless error messages, to AVOID
    logging.getLogger('pyembree').disabled = True

    scannet_data = DataScanNet(opt.dataset_scans_path)

    follow_up_file = os.path.join(opt.output_path, Pipe.follow_up_file_name)
    if not os.path.isfile(follow_up_file):
        follow_up_data = pd.DataFrame(index=scannet_data.scans)
    else:
        follow_up_data = pd.read_csv(follow_up_file, index_col=0)


    ##### -------------------------------------------------------------------------------------------------- #######
    p_registration = PipeRegistration(follow_up_data, scannet_data)
    p_registration.process(opt.output_path)
    #
    # ##### -------------------------------------------------------------------------------------------------- #######
    p_search_invalid_Poses= PipeSearchInvalidPoses(follow_up_data, scannet_data)
    p_search_invalid_Poses.process(opt.output_path)
    #
    # ##### -------------------------------------------------------------------------------------------------- #######
    p_test_propagate = PipeCalculatePropagator(follow_up_data, scannet_data, opt.interactions_path, opt.json_conf_execution_file)
    p_test_propagate.process(opt.output_path)
    #
    # p_test_propagate = PipeCalculatePropagator_Restricted(follow_up_data, scannet_data, opt.interactions_path, opt.json_conf_execution_file)
    # p_test_propagate.process(opt.output_path)
    #
    # ##### -------------------------------------------------------------------------------------------------- #######
    # p_test_propagator = TestPipePropagation(follow_up_data, scannet_data, opt.json_conf_execution_file)
    # p_test_propagator.process(opt.output_path)

    p_propagator_img =  PipePropagateOnImg(follow_up_data, scannet_data, opt.json_conf_execution_file, mask_width = 224, mask_height = 224, stride = 100, visualize= False)
    p_propagator_img.process(opt.output_path)