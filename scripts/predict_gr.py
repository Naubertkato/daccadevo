import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras import Model
from tensorflow.keras import layers

import numpy as np
import os


def get_predict_gr_daccadIndiv(daccadIndiv):
    new_model = tf.keras.models.load_model(os.path.abspath(os.getcwd()) + '/scripts/notebook/saved_model/my_model_for_gr')
    daccadIndiv = np.array(daccadIndiv[0:30]).reshape([1, 30])
    daccadIndiv = np.concatenate([daccadIndiv, np.mean(daccadIndiv[:, :5], axis=1).reshape((len(daccadIndiv), 1))], axis = 1)
    gr_prediction = new_model.predict(daccadIndiv)
    gr_prediction = np.argmax(gr_prediction[0])

    return gr_prediction
