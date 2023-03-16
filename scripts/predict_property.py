import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras import Model
from tensorflow.keras import layers

import numpy as np
import os

# not used
# myarray
def get_predict_mc(myarray):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model')
    myarray = myarray.reshape([1, 155])
    mc_prediction = new_model.predict(myarray)
    mc_prediction = mc_prediction[0][0]

    return mc_prediction

# not used
# myarray + eigenvalue
def get_predict_mc_eigenvalue(myarray, eigenvalue):

    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model_eigenvalue')
    nw_eigenvalue_data = np.append(myarray, eigenvalue)
    nw_eigenvalue_data = nw_eigenvalue_data.reshape([1, 156])
    mc_prediction = new_model.predict(nw_eigenvalue_data)
    mc_prediction = mc_prediction[0][0]

    return mc_prediction

# for memory capacity
# daccadIndiv (the value should be from 0 to 1)
def get_predict_mc_daccadIndiv(daccadIndiv):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model')
    daccadIndiv = np.array(daccadIndiv[0:30]).reshape([1, 30])
    daccadIndiv = np.concatenate([daccadIndiv, np.mean(daccadIndiv[:, :5], axis=1).reshape((len(daccadIndiv), 1))], axis = 1)
    mc_prediction = new_model.predict(daccadIndiv)
    mc_prediction = mc_prediction[0][0]

    return mc_prediction

# for kernel rank
def get_predict_kr_daccadIndiv(daccadIndiv):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model_for_kr')
    daccadIndiv = np.array(daccadIndiv[0:30]).reshape([1, 30])
    daccadIndiv = np.concatenate([daccadIndiv, np.mean(daccadIndiv[:, :5], axis=1).reshape((len(daccadIndiv), 1))], axis = 1)
    kr_prediction = new_model.predict(daccadIndiv)
    kr_prediction = np.argmax(kr_prediction[0])

    return kr_prediction

# for generalization rank
def get_predict_gr_daccadIndiv(daccadIndiv):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model_for_gr')
    daccadIndiv = np.array(daccadIndiv[0:30]).reshape([1, 30])
    daccadIndiv = np.concatenate([daccadIndiv, np.mean(daccadIndiv[:, :5], axis=1).reshape((len(daccadIndiv), 1))], axis = 1)
    gr_prediction = new_model.predict(daccadIndiv)
    gr_prediction = np.argmax(gr_prediction[0])

    return gr_prediction
