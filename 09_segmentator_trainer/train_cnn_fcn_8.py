
from keras_segmentation.models.fcn import fcn_8_resnet50, fcn_32_resnet50, fcn_8

if __name__ == "__main__":

    checkpoint_path = "/mnt/storage/home/csapo/scratch/train_cnn/checkpoints/fcn_8/fcn_8"

    train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/train_images/"
    annotated_train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_train_images/"

    val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/val_images/"
    annotated_val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_val_images/"

    input_height = 224
    input_width = 224

    n_classes = 2

    new_model = fcn_8(n_classes=n_classes, input_height=input_height, input_width=input_width)

    new_model.train(
        train_images=train_images,
        train_annotations=annotated_train_images,
        input_height=input_height,
        input_width=input_width,
        checkpoints_path=checkpoint_path,
        verify_dataset=False,
        epochs=15,
        batch_size=4,
        steps_per_epoch=60777 #total number of training data points(243,109) divided by the batch size
    )

    # out = model.predict_segmentation(
    #     inp="dataset1/images_prepped_test/0016E5_07965.png",
    #     out_fname="/tmp/out.png"
    # )
    #
    # import matplotlib.pyplot as plt
    #
    # plt.imshow(out)

    # evaluating the model
    print(new_model.evaluate_segmentation(inp_images_dir=val_images, annotations_dir=annotated_val_images))


