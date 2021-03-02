import argparse
import os

import tensorflow as tf

import pandas as pd

from keras_segmentation.models.segnet import segnet
from keras_segmentation.models.unet import unet

parser = argparse.ArgumentParser()
parser.add_argument('--interaction', required=True, help='Interaction to train')
parser.add_argument('--architecture', required=True, help='Interaction to train')

opt = parser.parse_args()


def read_scalar_from_tensorboard_log(path, scalar_to_display):
    """
    Read scalar from Tensorboard logs
    :param path: The path to logs
    :param scalar_to_display: Value to read from logs
    :return: list with all teh scalar per callback (step)
    """
    scalar_log = []
    files_dir = os.listdir(path)
    files_dir.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
    for file in files_dir:
        log_file = os.path.join(path, file)
        for e in tf.train.summary_iterator(log_file):
            for v in e.summary.value:
                if v.tag == scalar_to_display:
                    # this could correct if two files are in the directory
                    if e.step < len(scalar_log):
                        scalar_log[e.step] = v.simple_value
                    else:
                        scalar_log.append(v.simple_value)
    return scalar_log


if __name__ == "__main__":

    interaction = opt.interaction
    architecture = opt.architecture

    # for local test
    # checkpoint_dir = "/media/dougbel/Tezcatlipoca/dataset_analysis/mpi_routines/train_cnn/checkpoints_ghi"
    # test_images = "/media/dougbel/Tezcatlipoca/tmp_img_annotation/test_images"
    # annotated_test_images = f"/media/dougbel/Tezcatlipoca/tmp/annotation_test_images_imgs/{interaction}"

    checkpoint_dir = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/checkpoints_ghi"
    weights_dir = f"{checkpoint_dir}/{interaction}/{architecture}"
    logs_dir = f"{weights_dir}/{architecture}_logs"

    test_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/test_images/"
    annotated_test_images = f"/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/annotation_test_images_imgs/{interaction}"

    input_height = 224
    input_width = 224

    n_classes = 2

    if architecture == "segnet":
        new_model = segnet(n_classes=n_classes, input_height=input_height, input_width=input_width)
    elif architecture == "unet":
        new_model = unet(n_classes=n_classes, input_height=input_height, input_width=input_width)
    else:
        print("invalid architecture")
        exit()

    dir_logs_tra = os.path.join(logs_dir, "training")
    l_loss_tra = read_scalar_from_tensorboard_log(dir_logs_tra, "loss")
    l_acc_tra = read_scalar_from_tensorboard_log(dir_logs_tra, "acc")

    dir_logs_val = os.path.join(logs_dir, "validation")
    l_loss_val = read_scalar_from_tensorboard_log(dir_logs_val, "loss")
    l_acc_val = read_scalar_from_tensorboard_log(dir_logs_val, "acc")

    l_epoch = []
    l_arquitecture = []
    l_interaction = []
    l_frequency_weighted_IU = []
    l_mean_IU = []
    l_class_wise_IU_bck = []
    l_class_wise_IU_it = []

    for epoch in range(len(l_loss_tra)):
        weights_file = os.path.join(weights_dir, f"{architecture}.{epoch}")
        new_model.load_weights(weights_file)
        results = new_model.evaluate_segmentation(inp_images_dir=test_images, annotations_dir=annotated_test_images)

        l_interaction.append(interaction)
        l_epoch.append(epoch)
        l_arquitecture.append(architecture)

        l_frequency_weighted_IU.append(results['frequency_weighted_IU'])
        l_mean_IU.append(results['mean_IU'])
        l_class_wise_IU_bck.append(results['class_wise_IU'][0])
        l_class_wise_IU_it.append(results['class_wise_IU'][1])

    data = {'Interaction': l_interaction, 'Epoch': l_epoch, 'Arquiteture': l_arquitecture, 'Train_loss': l_loss_tra,
            'Validation_loss': l_loss_val, 'Train_acc': l_acc_tra, 'Validation_acc': l_acc_val,
            'Test_frequency_weighted_IU': l_frequency_weighted_IU, 'Test_mean_IU': l_mean_IU,
            'l_class_wise_IU_bck': l_class_wise_IU_bck, 'l_class_wise_IU_it': l_class_wise_IU_it}

    df = pd.DataFrame(data)
    df.to_excel(os.path.join(checkpoint_dir, f'{interaction}_{architecture}.xlsx'), index=False)
