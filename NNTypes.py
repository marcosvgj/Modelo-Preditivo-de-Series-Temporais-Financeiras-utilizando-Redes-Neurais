from keras import backend as K
from keras.layers import LSTM
from keras.layers.core import Dense, Dropout
from keras.models import Sequential


def custom_tanh(x):
    return 1.7159 * K.tanh((2 / 3) * x)


def mean_squared_error(y_true, y_pred):
    return K.mean(K.square(y_pred - y_true), axis=-1)



def mlp_type_1(neurons=64, dropout=0.4):
    model = Sequential()
    model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
    model.add(Dropout(dropout))
    model.add(Dense(neurons, input_shape=(1, 85), activation=custom_tanh, kernel_initializer='random_uniform'))
    model.add(Dense(10, activation='linear'))
    model.compile(loss=mean_squared_error,
                  optimizer='rmsprop',
                  metrics=[mean_squared_error])

    return model


def mlp_type_2(neurons=64, dropout=0.4):
    model = Sequential()
    model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
    model.add(Dense(neurons, input_shape=(1, 85), activation=custom_tanh, kernel_initializer='random_uniform'))
    model.add(Dropout(dropout))
    model.add(Dense(10, activation='linear'))
    model.compile(loss=mean_squared_error,
                  optimizer='rmsprop',
                  metrics=[mean_squared_error])

    return model


def mlp_type_3(neurons=64, dropout=0.4):
    model = Sequential()
    model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
    model.add(Dropout(dropout))
    model.add(Dense(neurons, input_shape=(1, 85), activation=custom_tanh, kernel_initializer='random_uniform'))
    model.add(Dropout(dropout))
    model.add(Dense(10, activation='linear'))
    model.compile(loss=mean_squared_error,
                  optimizer='rmsprop',
                  metrics=[mean_squared_error])

    return model


def lstm_type_1(dropout=0.4, neurons=64):
    model = Sequential()
    model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
    model.add(Dropout(dropout))
    model.add(LSTM(neurons, input_shape=(1, 85), activation=custom_tanh, return_sequences=True,
                   kernel_initializer='random_uniform'))
    model.add(Dense(10, activation='linear'))
    model.compile(loss=mean_squared_error,
                  optimizer='rmsprop',
                  metrics=[mean_squared_error])

    return model


def lstm_type_2(dropout=0.4, neurons=64):
    model = Sequential()
    model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
    model.add(Dropout(dropout))
    model.add(LSTM(neurons, input_shape=(1, 85), activation=custom_tanh, return_sequences=True,
                   kernel_initializer='random_uniform'))
    model.add(Dropout(dropout))
    model.add(Dense(10, activation='linear'))
    model.compile(loss=mean_squared_error,
                  optimizer='rmsprop',
                  metrics=[mean_squared_error])

    return model


def lstm_type_3(dropout=0.4, neurons=64):
    model = Sequential()
    model.add(Dense(85, input_shape=(1, 85), activation=custom_tanh))
    model.add(LSTM(neurons, input_shape=(1, 85), activation=custom_tanh, return_sequences=True,
                   kernel_initializer='random_uniform'))
    model.add(Dropout(dropout))
    model.add(Dense(10, activation='linear'))
    model.compile(loss=mean_squared_error,
                  optimizer='rmsprop',
                  metrics=[mean_squared_error])

    return model
