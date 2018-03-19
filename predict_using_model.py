import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"   # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from keras.models import model_from_json
from keras import backend as K
from scipy.misc import imresize
import itertools
import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Input
from keras.preprocessing.image import img_to_array, load_img

DATA_DIR = os.environ["DATA_DIR"]
VQA_IMAGES = os.path.join(DATA, "vqa")
IMAGENET_DIR = os.path.join(DATA, "imagenet")
MODELS_DIR = os.path.join(DATA_DIR, "models")

# load json and create model
json_file = open(os.path.join(MODELS_DIR, "resnet50-xgb-dot.pkl"), 'r')

loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights(os.path.join(MODELS_DIR, "imagenet_weights.h5"))

print("Loaded model from disk")
loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

original_image = plt.imread(os.path.join(IMAGE_DIR, "train2014/COCO_train2014_000000025162.jpg")).astype(np.float32)
original_image = imresize(original_image, (224,224))
original_image = np.divide(original_image, 256)
original_image =  np.expand_dims(original_image, axis=0)

image = plt.imread(os.path.join(IMAGE_DIR, "train2014/COCO_train2014_000000025162.jpg")).astype(np.float32)
image = imresize(image, (224, 224))
image = np.divide(image, 256)
image =  np.expand_dims(image, axis=0)

input_images = [original_image, image]

pred = loaded_model.predict(input_images ,batch_size=1, verbose=1)
print(pred)
