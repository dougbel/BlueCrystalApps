from keras_segmentation.models.model_utils import transfer_weights
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.models.pspnet import pspnet_50
from keras_segmentation.models.segnet import segnet

if __name__ == "__main__":

    checkpoint_path = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/checkpoints_ghi/segnet/segnet"

    train_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/train_images/"
    annotated_train_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/annotation_train_images_imgs/child_laying_child_laying/"

    val_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/test_images/"
    annotated_val_images = "/mnt/storage/home/csapo/scratch/analisys/mpi_routines/train_cnn/good_human_inter/annotation_test_images_imgs/child_laying_child_laying"

    input_height = 224
    input_width = 224

    n_classes = 2

    new_model = segnet(n_classes=n_classes, input_height=input_height, input_width=input_width)

    new_model.train(
        train_images=train_images,
        train_annotations=annotated_train_images,
        input_height=input_height,
        input_width=input_width,
        checkpoints_path=checkpoint_path,
        verify_dataset=False,
        epochs=25,
        batch_size=4,
        steps_per_epoch=10145  # total number of training data points for ghi (40581) divided by the batch size
    )

    print(new_model.evaluate_segmentation(inp_images_dir=val_images, annotations_dir=annotated_val_images))


