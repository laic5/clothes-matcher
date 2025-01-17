
# coding: utf-8

# In[ ]:

import os
import numpy as np
import pandas as pd
import pickle

from sklearn.metrics.pairwise import cosine_similarity


# In[ ]:

def get_top_k_indices(google_cnn_output, user_selected_ids, k):
    
    '''
    NOTE: user_selected_imgs NEEDS TO BE A LIST! Even if it's only 1 item.
    It does not handle 0 items at this moment.
    
    Both google_cnn_output and user_selected_imgs are output from the CNN and a np.array
    '''
    
    user_selected_imgs = google_cnn_output.loc[user_selected_ids]
    
    if len(google_cnn_output.shape) == 1:
        google_cnn_output = google_cnn_output.reshape(1, -1)
    if len(user_selected_imgs.shape) == 1:
        user_selected_imgs = user_selected_imgs.reshape(1, -1)
        
    similarity_results = np.zeros((len(user_selected_imgs), len(google_cnn_output)))

    #for idx, img in enumerate(user_selected_imgs):
    #    print(img.shape)
    #    similarity_results[idx,:] = cosine_similarity(img.reshape(1, -1), google_cnn_output)

    for i in range(len(user_selected_ids)):
        similarity_results[i,:] = cosine_similarity(user_selected_imgs.iloc[i,:].reshape(1,-1), google_cnn_output)

        
    if similarity_results.shape[0] == 1:
        sorted_indices = np.argsort(similarity_results[0])
    
    else:
        means = np.mean(similarity_results, axis=0)
        sorted_indices = np.argsort(means)
    
    if k > len(google_cnn_output):
        return (sorted_indices)
    
    top_indices = sorted_indices[-k:]

    return(list(reversed(top_indices)))

PICKLED_FILE = 'google1937.p'

with open(PICKLED_FILE, 'rb') as pickle_file:
    content = pickle.load(pickle_file)

google_cnn_output = pd.DataFrame(content)
user_selected_ids = [3,33]

output = get_top_k_indices(google_cnn_output, user_selected_ids, 5)
print(output)

