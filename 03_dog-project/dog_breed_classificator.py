import os
from glob import glob

import numpy as np
from PIL import ImageFile
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dropout, Flatten, Dense
from keras.models import Sequential
from keras.preprocessing import image
from keras.utils import np_utils
from sklearn.datasets import load_files
from keras.callbacks import ModelCheckpoint

from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

dir_img_dog_breed = os.path.join(os.getcwd(), 'data/dogImages')
dir_saved_models = os.path.join(os.getcwd(), 'data/saved_models')

if not os.path.exists(dir_saved_models):
    os.makedirs(dir_saved_models)


# define function to load train, test, and validation datasets
def load_dataset(path):
    data = load_files(path)
    dog_files = np.array(data['filenames'])
    dog_targets = np_utils.to_categorical(np.array(data['target']), 133)
    return dog_files, dog_targets


# load train, test, and validation datasets
train_files, train_targets = load_dataset(os.path.join(dir_img_dog_breed, 'train'))
valid_files, valid_targets = load_dataset(os.path.join(dir_img_dog_breed, 'valid'))
test_files, test_targets = load_dataset(os.path.join(dir_img_dog_breed, 'test'))

# load list of dog names
dog_names = [item[20:-1] for item in sorted(glob( os.path.join(dir_img_dog_breed, "train/*/")))]

# print statistics about the dataset
print('There are %d total dog categories.' % len(dog_names))
print('There are %s total dog images.\n' % len(np.hstack([train_files, valid_files, test_files])))
print('There are %d training dog images.' % len(train_files))
print('There are %d validation dog images.' % len(valid_files))
print('There are %d test dog images.' % len(test_files))

ImageFile.LOAD_TRUNCATED_IMAGES = True


def path_to_tensor(img_path):
    # loads RGB image as PIL.Image.Image type
    img = image.load_img(img_path, target_size=(224, 224))
    # convert PIL.Image.Image type to 3D tensor with shape (224, 224, 3)
    x = image.img_to_array(img)
    # convert 3D tensor to 4D tensor with shape (1, 224, 224, 3) and return 4D tensor
    return np.expand_dims(x, axis=0)


def paths_to_tensor(img_paths):
    list_of_tensors = [path_to_tensor(img_path) for img_path in img_paths]
    return np.vstack(list_of_tensors)


print("Pre-process the data for Keras")
train_tensors = paths_to_tensor(train_files).astype('float32') / 255
valid_tensors = paths_to_tensor(valid_files).astype('float32') / 255
test_tensors = paths_to_tensor(test_files).astype('float32') / 255

print("Arquitecture definition")

model = Sequential()

model.add(Conv2D(filters=16, kernel_size=2, padding='same', activation='relu',
                 input_shape=(224, 224, 3)))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=32, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Conv2D(filters=64, kernel_size=2, padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(500, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(133, activation='softmax'))

model.summary()

print("COMPILE MODEL")
model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

### specify the number of epochs that you would like to use to train the model.
epochs = 10
print("TRAIN model")
checkpointer = ModelCheckpoint(filepath=os.path.join(dir_saved_models, 'weights.best.from_scratch.hdf5'), verbose=1,
                               save_best_only=True)

model.fit(train_tensors, train_targets, validation_data=(valid_tensors, valid_targets), epochs=epochs, batch_size=20,
          callbacks=[checkpointer], verbose=1)

# LOAD model with best validation loss
model.load_weights(os.path.join(dir_saved_models,'weights.best.from_scratch.hdf5'))

print("TEST model")
# get index of predicted dog breed for each image in test set
dog_breed_predictions = [np.argmax(model.predict(np.expand_dims(tensor, axis=0))) for tensor in test_tensors]

# report test accuracy
test_accuracy = 100 * np.sum(np.array(dog_breed_predictions) == np.argmax(test_targets, axis=1)) / len(
    dog_breed_predictions)
print('Test accuracy: %.4f%%' % test_accuracy)
