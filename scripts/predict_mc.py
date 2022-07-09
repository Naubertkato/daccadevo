import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras import Model
from tensorflow.keras import layers

import numpy as np

def get_predict_mc(myarray):

    new_model = tf.keras.models.load_model('./notebook/saved_model/my_model')
    mc_prediction = new_model.predict(myarray)

    return mc_prediction

def get_predict_mc_eigenvalue(myarray, eigenvalue):

    new_model = tf.keras.models.load_model('./notebook/saved_model/my_model_eigenvalue')
    nw_eigenvalue_data = np.append(myarray, eigenvalue)
    mc_prediction = new_model.predict(nw_eigenvalue_data)

    return mc_prediction
