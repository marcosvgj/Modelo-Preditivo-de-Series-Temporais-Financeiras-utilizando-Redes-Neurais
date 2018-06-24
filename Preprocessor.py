#!/usr/bin/python


from pandas import DataFrame
from pandas import concat
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np


class PreProcessor:
    def __init__(self, data):
        self.dataset = {}
        self.data = data
        self.scaler = None

    def normalization(self):
        columns = self.data.columns
        self.scaler = MinMaxScaler(feature_range=(-1, 1))
        self.data = self.scaler.fit_transform(self.data)
        self.data = pd.DataFrame(self.data, columns=columns)

    def split_train_test(self, percentual_train=0.90):
        tam_treino = int(len(self.data) * percentual_train)
        self.dataset['train'], self.dataset['test'] = self.data[0:tam_treino], self.data[tam_treino:len(self.data)]

    def sliding_window(self, x_in=1, y_out=1, drop_nan=True):

        df = DataFrame(self.data)
        cols, names = list(), list()

        for i in range(x_in, 0, -1):
            aux_1 = df.shift(-i)

            cols.append(aux_1)
            for j in aux_1.keys():
                names += [j + ' (t)']

        for i in range(1, y_out + 1):
            aux = df.shift(-i)
            cols.append(aux)
            # cols.append(df.shift(-i))
            if i == 1:
                for j in aux.keys():
                    names += [j + ' (t+1)']

            else:
                for j in aux.keys():
                    names += [j + ' (t+%d)' % i]

        agg = concat(cols, axis=1)
        agg.columns = names

        if drop_nan:
            agg.dropna(inplace=True)
        self.data = agg

    def split_in_out(self, slide_window_in, col):
        """slide_window_in refere-se a quantidade de pontos da série utilizado como entrada.
        No caso o modelo atual trabalha com 17 variáveis"""
        index = 1

        for j in ([self.dataset['train'], self.dataset['test']]):

            x = j.iloc[:, :slide_window_in * col]
            y_list = []
            for i in j.keys():
                if i[:11] == 'closing (t+':
                    y_list.append(i)
            y = j[y_list]

            if index == 1:
                self.dataset['train_x'] = DataFrame(x)
                self.dataset['train_y'] = y
            else:
                self.dataset['test_x'] = DataFrame(x)
                self.dataset['test_y'] = y

            index += 1

    def set_numpy_format(self):

        def reshape_data(data):
            return np.reshape(data, (data.shape[0], 1, data.shape[1]))

        for k in ('train', 'test'):
            self.dataset[k + '_x'] = np.array(self.dataset[k + '_x'])
            self.dataset[k + '_x'] = reshape_data(self.dataset[k + '_x'])

            self.dataset[k + '_y'] = np.array(self.dataset[k + '_y'])
            self.dataset[k + '_y'] = reshape_data(self.dataset[k + '_y'])

    def get_data(self):
        return self.dataset

    def get_train_x(self):
        return self.dataset['train_x']

    def get_train_y(self):
        return self.dataset['train_y']

    def get_test_x(self):
        return self.dataset['test_x']

    def get_test_y(self):
        return self.dataset['test_y']

    def get_scaler(self):
        return self.scaler
