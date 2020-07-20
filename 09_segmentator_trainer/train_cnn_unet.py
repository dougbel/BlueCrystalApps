from keras_segmentation.models.model_utils import transfer_weights
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.models.pspnet import pspnet_50
from keras_segmentation.models.unet import unet

if __name__ == "__main__":

    checkpoint_path = "/mnt/storage/home/csapo/scratch/train_cnn/checkpoints/unet/unet"

    train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/train_images/"
    annotated_train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_train_images/"

    val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/val_images/"
    annotated_val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_val_images/"

    input_height = 224
    input_width = 224

    n_classes = 2

    new_model = unet(n_classes=n_classes, input_height=input_height, input_width=input_width)

    new_model.train(
        train_images=train_images,
        train_annotations=annotated_train_images,
        input_height=input_height,
        input_width=input_width,
        checkpoints_path=checkpoint_path,
        verify_dataset=False,
        epochs=15,
        batch_size=4,
        steps_per_epoch=60777  # total number of training data points(243,109) divided by the batch size
    )

    print(new_model.evaluate_segmentation(inp_images_dir=val_images, annotations_dir=annotated_val_images))


