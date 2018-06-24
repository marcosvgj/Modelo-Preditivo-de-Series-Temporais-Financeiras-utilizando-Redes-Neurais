from keras import backend as K
from keras.layers import LSTM
from keras.layers.core import Dense, Dropout
from keras.models import Sequential
from sklearn.metrics import mean_squared_error


def custom_tanh(x):
    return 1.7159 * K.tanh((2 / 3) * x)


class NNTypes:
    def __init__(self):
        self.metric = mean_squared_error
        self.custom_tanh = custom_tanh

    def mlp_type_1(self, neurons=64, dropout=0.4):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=self.custom_tanh))
        model.add(Dropout(dropout))
        model.add(Dense(neurons, input_shape=(1, 85), activation=self.custom_tanh, kernel_initializer='random_uniform'))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=self.metric,
                      optimizer='rmsprop',
                      metrics=[self.metric])

        return model

    def mlp_type_2(self, neurons=64, dropout=0.4):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=self.custom_tanh))
        model.add(Dense(neurons, input_shape=(1, 85), activation=self.custom_tanh, kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=self.metric,
                      optimizer='rmsprop',
                      metrics=[self.metric])

        return model

    def mlp_type_3(self, neurons=64, dropout=0.4):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=self.custom_tanh))
        model.add(Dropout(dropout))
        model.add(Dense(neurons, input_shape=(1, 85), activation=self.custom_tanh, kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=self.metric,
                      optimizer='rmsprop',
                      metrics=[self.metric])

        return model

    def lstm_type_1(self, dropout=0.4, neurons=64):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=self.custom_tanh))
        model.add(Dropout(dropout))
        model.add(LSTM(neurons, input_shape=(1, 85), activation=self.custom_tanh, return_sequences=True,
                       kernel_initializer='random_uniform'))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=self.metric,
                      optimizer='rmsprop',
                      metrics=[self.metric])

        return model

    def lstm_type_2(self, dropout=0.4, neurons=64):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=self.custom_tanh))
        model.add(Dropout(dropout))
        model.add(LSTM(neurons, input_shape=(1, 85), activation=self.custom_tanh, return_sequences=True,
                       kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=self.metric,
                      optimizer='rmsprop',
                      metrics=[self.metric])

        return model

    def lstm_type_3(self, dropout=0.4, neurons=64):
        model = Sequential()
        model.add(Dense(85, input_shape=(1, 85), activation=self.custom_tanh))
        model.add(LSTM(neurons, input_shape=(1, 85), activation=self.custom_tanh, return_sequences=True,
                       kernel_initializer='random_uniform'))
        model.add(Dropout(dropout))
        model.add(Dense(10, activation='linear'))
        model.compile(loss=self.metric,
                      optimizer='rmsprop',
                      metrics=[self.metric])

        return model
