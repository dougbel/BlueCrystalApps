from keras_segmentation.models.model_utils import transfer_weights
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.models.pspnet import pspnet_50
from keras_segmentation.models.fcn import fcn_8_resnet50

if __name__ == "__main__":

    checkpoint_path = "/mnt/storage/home/csapo/scratch/for_testing/segmentation/checkpoints/fcn/fcn_8_resnet50"

    train_images = "/mnt/storage/home/csapo/scratch/for_testing/segmentation/images_prepped_train/"
    annotated_train_images = "/mnt/storage/home/csapo/scratch/for_testing/segmentation/annotations_prepped_train/"

    val_images = "/mnt/storage/home/csapo/scratch/for_testing/segmentation/images_prepped_test/"
    annotated_val_images = "/mnt/storage/home/csapo/scratch/for_testing/segmentation/annotations_prepped_test/"

    input_height = 360
    input_width = 480

    model = fcn_8_resnet50(n_classes=51, input_height=input_height, input_width=input_width)

    model.train(
        train_images=train_images,
        train_annotations=annotated_train_images,
        input_height=input_height,
        input_width=input_width,
        checkpoints_path=checkpoint_path,
        verify_dataset=True,
        epochs=5
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
    print(model.evaluate_segmentation(inp_images_dir=val_images, annotations_dir=annotated_val_images))


