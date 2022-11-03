import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras import Model
from tensorflow.keras import layers

import numpy as np
import osmyarray

# myarray -> daccadIndiv
def get_predict_mc(myarray):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model')
    myarray = myarray.reshape([1, 155])
    mc_prediction = new_model.predict(myarray)
    mc_prediction = mc_prediction[0][0]

    return mc_prediction

def get_predict_mc_daccadIndiv(daccadIndiv):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model')
    daccadIndiv = daccadIndiv.reshape([1, 155])
    mc_prediction = new_model.predict(daccadIndiv)
    mc_prediction = mc_prediction[0][0]

    return mc_prediction

def get_predict_mc_eigenvalue(myarray, eigenvalue):

    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model_eigenvalue')
    nw_eigenvalue_data = np.append(myarray, eigenvalue)
    nw_eigenvalue_data = nw_eigenvalue_data.reshape([1, 156])
    mc_prediction = new_model.predict(nw_eigenvalue_data)
    mc_prediction = mc_prediction[0][0]

    return mc_prediction
