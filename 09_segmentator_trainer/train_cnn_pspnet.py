import tensorflow as tf
from keras_segmentation.models.model_utils import transfer_weights
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.models.pspnet import pspnet_50

if __name__ == "__main__":

    checkpoints_path = "/mnt/storage/home/csapo/scratch/train_cnn/checkpoints/psp_net/psp_net"

    train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/train_images/"
    annotated_train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_train_images/"

    input_height = 224
    input_width = 224

    epochs = 40
    n_classes = 2


    # to measure the quantity of GPU used
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True

    pretrained_model = pspnet_50_ADE_20K()

    new_model = pspnet_50(n_classes=n_classes)

    transfer_weights(pretrained_model, new_model)  # transfer weights from pre-trained model to your model

    H = new_model.train(
        checkpoints_path=checkpoints_path,
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
        batch_size=4,
    )

    # evaluating the model
    val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/val_images/"
    annotated_val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_val_images/"
    print(new_model.evaluate_segmentation(inp_images_dir=val_images, annotations_dir=annotated_val_images))
