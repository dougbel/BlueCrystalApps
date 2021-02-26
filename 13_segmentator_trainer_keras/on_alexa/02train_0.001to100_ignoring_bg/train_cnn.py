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
parser.add_argument('--analysis_intersection_percentages', required=True, help='1to100')
parser.add_argument('--interactions_set', required=True, help='Indicate set of interactions to use')
parser.add_argument('--ignore_background', required=True, help='Indicate if background is ignored during training')

opt = parser.parse_args()

if __name__ == "__main__":

    interaction = opt.interaction
    architecture = opt.architecture
    interactions_set = opt.interactions_set
    analysis_intersection_percentages = opt.analysis_intersection_percentages
    ignore_background = opt.ignore_background == 'True'

    # to measure the quantity of GPU used
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    base_path = f"/media/alexa/DATA/Abel/train_cnn/{interactions_set}/{analysis_intersection_percentages}"

    chk_name = "checkpoints_ignore_background" if ignore_background else "checkpoints"

    checkpoint_path = f"{base_path}/{chk_name}/{interaction}/{architecture}/{architecture}"

    train_images = f"{base_path}/train_images/"
    annotated_train_images = f"{base_path}/annotation_train_images_imgs/{interaction}/"

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
        ignore_zero_class=ignore_background,
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
