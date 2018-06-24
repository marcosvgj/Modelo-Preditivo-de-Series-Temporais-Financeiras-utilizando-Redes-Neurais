#!/usr/bin/python

import abc
from keras import backend as K
from keras.layers import LSTM
from keras.layers.core import Dense, Dropout
from keras.models import Sequential


def custom_tanh(x):
    return 1.7159 * K.tanh((2 / 3) * x)


def mean_squared_error(y_true, y_pred):
    """

    :param y_true:
    :param y_pred:
    :return:
    """
    return K.mean(K.square(y_pred - y_true), axis=-1)


class Model:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def topology(self):
        "Topologia da rede construída"


class MLPType1(Model):
    def topology(self, neurons=64, dropout=0.4):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
        model.add(Dropout(dropout))
        model.add(Dense(neurons, input_shape=(1, 85), activation=custom_tanh, kernel_initializer='random_uniform'))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=mean_squared_error,
                      optimizer='rmsprop',
                      metrics=[mean_squared_error])

        return model


class MLPType2(Model):
    def topology(self, neurons=64, dropout=0.4):
        model = Sequential()
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh))
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh, kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=mean_squared_error,
                      optimizer='rmsprop',
                      metrics=[mean_squared_error])

        return model


class MLPType3(Model):
    def topology(self, neurons=64, dropout=0.4):
        model = Sequential()
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh))
        model.add(Dropout(dropout))
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh, kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=mean_squared_error,
                      optimizer='rmsprop',
                      metrics=[mean_squared_error])

        return model


class LSTMType1(Model):
    def topology(self, dropout=0.4, neurons=64):
        model = Sequential()
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh))
        model.add(Dropout(dropout))
        model.add(LSTM(input_shape=(1, 85), activation=custom_tanh, return_sequences=True,
                       kernel_initializer='random_uniform'))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=mean_squared_error,
                      optimizer='rmsprop',
                      metrics=[mean_squared_error])

        return model


class LSTMType2(Model):
    def topology(self, dropout=0.4, neurons=64):
        model = Sequential()
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh))
        model.add(Dropout(dropout))
        model.add(LSTM(input_shape=(1, 85), activation=custom_tanh, return_sequences=True,
                       kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=mean_squared_error,
                      optimizer='rmsprop',
                      metrics=[mean_squared_error])

        return model


class LSTMType3(Model):
    def topology(self, dropout=0.4, neurons=64):
        model = Sequential()
        model.add(Dense(input_shape=(1, 85), activation=custom_tanh))
        model.add(LSTM(input_shape=(1, 85), activation=custom_tanh, return_sequences=True,
                       kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=mean_squared_error,
                      optimizer='rmsprop',
                      metrics=[mean_squared_error])

        return model
