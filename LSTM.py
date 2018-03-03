from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras import backend as K
from keras.layers import LSTM


class LSTM:
    def __init__(self):
        print("Iniciando o LSTM Recurrent Neural Network Model")

    def custom_tanh(self, x):
        return 1.7159 * K.tanh((2 / 3) * x)

    def coeff_determination(self, y_true, y_pred):
        SS_res = K.sum(K.square(y_true - y_pred))
        SS_tot = K.sum(K.square(y_true - K.mean(y_true)))
        return (1 - SS_res / (SS_tot + K.epsilon()))

    def mean_squared_error(y_true, y_pred):
        return K.mean(K.square(y_pred - y_true), axis=-1)

    def build_model(self, train_X, train_y, test_X, test_y):
        model = Sequential()

        model.add(
            LSTM(32, input_shape=(train_X.shape[1], train_X.shape[2]), activation=self.custom_tanh,
                 return_sequences=True))

        model.add(Dropout(0.475))

        model.add(
            LSTM(32, input_shape=(train_X.shape[1], train_X.shape[2]), activation=self.custom_tanh,
                 return_sequences=True))

        model.add(Dense(1, activation='linear'))

        model.compile(loss='mean_squared_error',
                      optimizer='rmsprop',
                      metrics=[LSTM.mean_squared_error])

        history = model.fit(train_X,
                            train_y,
                            epochs=1000,
                            batch_size=64,
                            verbose=2,
                            validation_data=(test_X, test_y))

        return model, history
