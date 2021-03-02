import argparse

from keras_segmentation.models.segnet import segnet
from keras_segmentation.models.unet import unet

parser = argparse.ArgumentParser()
parser.add_argument('--interaction', required=True, help='Interaction to train')
parser.add_argument('--architecture', required=True, help='Interaction to train')


opt = parser.parse_args()

if __name__ == "__main__":

    interaction = opt.interaction
    architecture = opt.architecture

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
