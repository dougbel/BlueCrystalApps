from keras_segmentation.models.model_utils import transfer_weights
from keras_segmentation.pretrained import pspnet_50_ADE_20K
from keras_segmentation.models.pspnet import pspnet_50
from keras_segmentation.models.fcn import fcn_8_resnet50

if __name__ == "__main__":
    checkpoint_path = "/mnt/storage/home/csapo/scratch/train_cnn/checkpoints/psp_net/psp_net"

    train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/train_images/"
    annotated_train_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_train_images/"

    val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/val_images/"
    annotated_val_images = "/mnt/storage/home/csapo/scratch/train_cnn/imgs/annotation_val_images/"

    input_height = 224
    input_width = 224

    n_classes = 2

    pretrained_model = pspnet_50_ADE_20K()

    new_model = pspnet_50(n_classes=n_classes, input_height=input_height, input_width=input_width)

    transfer_weights(pretrained_model, new_model)  # transfer weights from pre-trained model to your model

    new_model.train(
        checkpoints_path=checkpoint_path,
        auto_resume_checkpoint=False,
        ignore_zero_class=False,
        verify_dataset=False,

        validate=True,  # change to false if dont want to validate
        val_images=val_images,
        val_annotations=annotated_val_images,
        val_batch_size=4,
        val_steps_per_epoch=5236,  # total number of VALIDATION data (20942) divided by the batch size

        train_images=train_images,
        train_annotations=annotated_train_images,
        input_height=input_height,
        input_width=input_width,
        epochs=5,
        batch_size=4,
        steps_per_epoch=60778  # total number of TRAINING data points(243109) divided by the batch size
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
