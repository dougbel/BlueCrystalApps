import sys
import argparse
import os
import collections
from tqdm import tqdm

import cv2
import numpy as np
import logging


def sort_files(file_names):
    """Sort files by the number of frame, This by following a pattern as image_frame_[num_frame]_[extra_info].[extension]

    Args:
        file_names (list strings): List of filename to order

    Returns:
        list string: ordered list by [num_frame] in the string pattern
    """
    return sorted(file_names, key=lambda value: int(value[12:12 + value[12:].find('_')]))


def list_npy_file(input_path):
    return sort_files([each for each in os.listdir(input_path) if each.endswith('.npy')])


def compress_npy_files_in_a_path(input_path, output_path, output_file_name):
    file_names = list_npy_file(input_path)

    ####################################################################################################################
    # Compressing files
    ordered_dict = collections.OrderedDict()
    for file_name in file_names:
        try:
            ordered_dict[file_name] = np.load(os.path.join(input_path, file_name))
        except:
            logging.error(file_name + " Bad npy file (ValueError: total size of new array must be unchanged)")
            print(file_name + " Bad npy file (ValueError: total size of new array must be unchanged)")
    # from 585 MB to 266 MB
    output_file = os.path.join(output_path, output_file_name)

    if not os.path.isfile(output_file):
        np.savez_compressed(output_file, **ordered_dict)
    else:
        logging.info("npz file ALREADY calculated")
        print("npz file ALREADY calculated")


def verify_data_integrity_between_compression_and_npy_data(input_path, npz_file_path, npz_file_name):
    file_names = list_npy_file(input_path)
    ####################################################################################################################
    # Test compression is correct
    data_compiled = np.load(os.path.join(npz_file_path, npz_file_name))

    # data in compressed is equal to the one in file
    for key in data_compiled.keys():
        data_from_file = np.load(os.path.join(input_path, key))
        if not np.all(data_from_file == data_compiled[key]):
            logging.error("Difference between compressed data and npy files ")
            print("Difference between compressed data and npy files ")
            return False
    logging.info("SUCCESS: compressed data and files are equals")

    # number of files is equal to the number in compressed data
    if len(file_names) != len(data_compiled.keys()):
        logging.error("Difference between number of compressed arrays and npy files ")
        print("Difference between number of compressed arrays and npy files ")
        return False
    logging.info("SUCCESS: number of compressed numpy array and files are equals")
    return True


def compress_to_npz_and_remove_npy_files(input_path, npz_file_name):
    list_npy_files = list_npy_file(input_path)
    if len(list_npy_files) > 0:
        compress_npy_files_in_a_path(input_path, input_path, npz_file_name)
        verified = verify_data_integrity_between_compression_and_npy_data(input_path, input_path, npz_file_name)
        if verified is True:
            [os.remove(os.path.join(input_path, file)) for file in list_npy_files]


parser = argparse.ArgumentParser()
parser.add_argument('--src_path', required=True, help='Path to output')

opt = parser.parse_args()
print(opt)

if __name__ == "__main__":

    id_task = int(os.getenv('SLURM_ARRAY_TASK_ID'))
    src_path = opt.src_path

    logging_file = os.path.join(".", 'compressing_npy_'+str(id_task)+'.log')
    logging.basicConfig(filename=logging_file, filemode='a', level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

    npz_file_name = "scores_1.npz"
    path = os.path.join(src_path, "task_"+str(id_task))

    # list of files in path
    if os.path.isdir(path):
        imgs_paths = [os.path.join(path, sub_path) for sub_path in os.listdir(path) if
                      sub_path.endswith('_img_segmentation_w224_x_h224')]
        for img_path in tqdm(imgs_paths, desc="working paths"):
            # list of scenes in a given folder with images
            scenes = os.listdir(img_path)
            logging.info(img_path)
            print(img_path)
            for scene in tqdm(scenes, desc="scenes"):
                scene_path = os.path.join(path, img_path, scene)
                logging.info("PROCESSING " + scene_path)
                compress_to_npz_and_remove_npy_files(scene_path, npz_file_name)
                logging.info("DONE " + scene_path)
