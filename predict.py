
# coding: utf-8

# In[1]:

import os
import numpy as np
import pandas as pd
from tqdm import tqdm 
from PIL import Image


# In[8]:

import tensorflow as tf
import keras

from keras.applications import ResNet50
from keras.models import Model
from keras.layers import Dense, GlobalAveragePooling2D
from keras.optimizers import SGD
from keras.models import load_model

from tqdm import tqdm

from sklearn.metrics.pairwise import cosine_similarity
import pickle

import argparse


# In[4]:

def remove_softmax(model):
    model.layers.pop() # Get rid of the classification layer
    model.outputs = [model.layers[-1].output]
    model.layers[-1].outbound_nodes = []
    
    return model


# In[5]:

def get_cnn_output(model, ims):
    # ims is np array
    if len(ims.shape) == 1:
        ims = ims.reshape(1, -1)
    
    return (model.predict(ims))


# In[ ]:

parser = argparse.ArgumentParser()
parser.add_argument('--model', dest='model', default='resnet.h5', type=str)
parser.add_argument('--fname', dest='fname', default='pred.p', type=str)
parser.add_argument('--dir', dest='dir', default='images/', type=str)

args = parser.parse_args()


# In[6]:

#model2 = ResNet50(weights='imagenet') # using imagenet for now -- comment this, and uncomment next after implementing argparse
model2 = load_model(args.model)

model2 = remove_softmax(model2)


# In[10]:

# load images from image directory

def read_images_from_dir(directory):
    '''
    Reads in all images in a directory.
    Can deal with 1 nested directory
    Converts file --> PIL image --> np array
    '''
    directory_contents_list  = os.listdir(directory)

    ims = []
    try:
        if os.path.isdir(os.path.join(directory, directory_contents_list[0])): # there's another directory
            # go down another layer
            for direc in directory_contents_list:
                # list all the images in the directory
                images_list = os.listdir(os.path.join(directory, direc))

                # open the images and resize
                ims.extend([np.array(Image.open(os.path.join(directory, direc, im)), dtype=np.float64).resize((224,224)) for im in images_list])

        else: # directly open up the images
            ims = [np.array(Image.open(os.path.join(directory, file)), dtype=np.float64).resize((224,224)) for file in directory_contents_list]
    except:
        print("Issue loading the images!")
        
    return ims


# In[ ]:

directory = args.dir
image_list = read_images_from_dir(directory)
preds = get_cnn_output(model2, image_list)


# In[ ]:

#cPickle.dump(preds, open(args.fname, "wb"))

f = open(args.fname, 'wb')   # 'wb' instead 'w' for binary file
pickle.dump(preds)       # -1 specifies highest binary protocol
f.close() 

