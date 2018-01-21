
# coding: utf-8

# In[46]:

import os
import numpy as np
import pandas as pd
from tqdm import tqdm 
from PIL import Image
from imagenet_utils import preprocess_input


# In[22]:

# file structure is ./data/small/[clothing_category]/[image no.]

train_directory = './data/small/'
# Form list of training images names
directory_list  = os.listdir(train_directory)
# Convert to 224 x 224 images

ims = []

for directory in directory_list:
    # list all the images in the directory
    images_list = os.listdir(os.path.join(train_directory, directory))
    
    # open the images and resize
    ims.extend([Image.open(os.path.join(train_directory, directory, im)).resize((224,224)) for im in images_list])


# In[27]:

num_pics = len(ims)


# In[30]:

def get_category(string):
    # split by underscore
    # get last element
    temp = string.split("_")
    return temp[-1]


# In[36]:

labs = []
for direc in directory_list:
    category = get_category(direc)
    
    images_list = os.listdir(os.path.join(train_directory, direc))

    for i in range(len(images_list)):
        labs.append(category)


# ### Now: All the images stored under "ims" and all the simplified labels stored under "labs"

# In[41]:

# one hot encoding

s = pd.Series(labs)
one_hot_categories = pd.get_dummies(s)


# In[81]:

imlist = np.array([np.array(im, dtype=np.float64) for im in ims])


# # Resnet Time

# In[60]:

import tensorflow as tf
import keras

from keras.applications import ResNet50
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.optimizers import SGD

from tqdm import tqdm
import glob


# In[51]:

IM_HEIGHT = 224
IM_WIDTH = 224
NB_EPOCHS = 1
BAT_SIZE = 16
FC_SIZE = 500 # May need to train this parameter

nb_classes = len(set(labs))


# In[47]:

def setup_to_transfer_learn(model, base_model):
    """Freeze all layers and compile the model"""
    adam = keras.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    for layer in base_model.layers:
        layer.trainable = False
        model.compile(optimizer='adam',    
                    loss='categorical_crossentropy', 
                    metrics=['accuracy'])


# In[58]:

def add_new_last_layer(base_model, nb_classes):
    """Add last layer to the convnet
    Args:
    base_model: keras model excluding top
    nb_classes: # of classes
    Returns:
    new keras model with last layer
    """
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(FC_SIZE, activation='relu')(x) #new FC layer, random init
    predictions = Dense(nb_classes, activation='softmax')(x) #new softmax layer
    model = Model(inputs = base_model.input, outputs = predictions)
    return model


# In[93]:

def resnet_train(images, labels):
    
    base_model = ResNet50(weights='imagenet', include_top=False)
    model = add_new_last_layer(base_model, nb_classes)

    setup_to_transfer_learn(model, base_model)

    history = model.fit(images, labels)
    model.save("resnet.h5")
    
    return history

h = tqdm(resnet_train(imlist, one_hot_categories.values))

