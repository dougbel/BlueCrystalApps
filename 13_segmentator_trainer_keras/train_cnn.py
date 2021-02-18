import argparse

import tensorflow as tf

# from keras_segmentation.models.fcn import fcn_8, fcn_32_resnet50
# from keras_segmentation.models.model_utils import transfer_weights
# from keras_segmentation.models.pspnet import pspnet_50
from keras_segmentation.models.segnet import segnet
from keras_segmentation.models.unet import unet
# from keras_segmentation.pretrained import pspnet_50_ADE_20K

parser = argparse.ArgumentParser()
parser.add_argument('--interaction', required=True, help='Interaction to train')
parser.add_argument('--architecture', required=True, help='Interaction to train')


opt = parser.parse_args()

if __name__ == "__main__":

    interaction = opt.interaction
    architecture = opt.architecture

    # to measure the quantity of GPU used
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    checkpoint_path = f"/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/checkpoints_ghi/{interaction}/{architecture}/{architecture}"

    train_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/train_images/"
    annotated_train_images = f"/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/annotation_train_images_imgs/{interaction}/"

    val_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/test_images/"
    annotated_val_images = f"/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/annotation_test_images_imgs/{interaction}"

    input_height = 224
    input_width = 224

    n_classes = 2

    epochs = 25

    if architecture == "segnet":
        new_model = segnet(n_classes=n_classes, input_height=input_height, input_width=input_width)
    elif architecture == "unet":
        new_model = unet(n_classes=n_classes, input_height=input_height, input_width=input_width)
    # elif architecture == "fcn_8":
    #     new_model = fcn_8(n_classes=n_classes, input_height=input_height, input_width=input_width)
    # elif architecture == "fcn_32_resnet50":
    #     new_model = fcn_32_resnet50(n_classes=n_classes, input_height=input_height, input_width=input_width)
    # elif architecture == "pspnet_50":
    #     pretrained_model = pspnet_50_ADE_20K()
    #     new_model = pspnet_50(n_classes=n_classes)
    #     transfer_weights(pretrained_model, new_model)  # transfer weights from pre-trained model to your model
    else:
        print("invalid architecture")
        exit()



    new_model.train(
        checkpoints_path=checkpoint_path,
        auto_resume_checkpoint=True,
        ignore_zero_class=False,
        verify_dataset=False,
        validate=True,  # change to false if dont want to validate
        validation_split=.2,
        train_images=train_images,
        train_annotations=annotated_train_images,
        input_height=input_height,
        input_width=input_width,
        epochs=epochs,
        batch_size=4
    )

    print(f"Training {architecture} on {interaction} results after {epochs} epochs: ")
    print(new_model.evaluate_segmentation(inp_images_dir=val_images, annotations_dir=annotated_val_images))
