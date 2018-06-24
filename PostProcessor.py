from pandas import DataFrame
import pandas as pd
import os
from matplotlib import pyplot
from numpy import array
import numpy as np


def consolidar_serie(serie):
    lista_consolidada = [list(serie[0])[0]]
    for item in serie[1:]:
        lista_consolidada.append(item[4])

    return lista_consolidada


class PostProcessor:
    def __init__(self, data, model, config, scaler):
        self.raw_model = model
        self.data = data
        self.scaler = scaler
        self.trainPredict_v2 = []
        self.testPredict_v2 = []
        self.configuration = config
        self.path = 'C:/Users/Marcos/PycharmProjects/tradingproject/resultados/'

    def training_best_nn(self):
        self.raw_model(neurons=self.configuration['Neurons'], dropout=self.configuration['Dropout']) \
            .fit(self.data['train_x'],
                 self.data['train_y'],
                 batch_size=32,
                 epochs=self.configuration['Epochs'],
                 verbose=2,
                 validation_data=(self.data['test_x'], self.data['test_y']))

    def train_model(self):
        train_predict = self.raw_model.predict(self.data['train_x'])
        self.trainPredict_v2 = train_predict.reshape(train_predict.shape[0], train_predict.shape[2])

        test_predict = self.raw_model.predict(self.data['test_x'])
        self.testPredict_v2 = test_predict.reshape(test_predict.shape[0], test_predict.shape[2])

    def plot_nn_result(self):
        pyplot.figure(figsize=(20.5, 3))
        pyplot.plot(consolidar_serie(np.array(self.data['treino']['closing (t)'])), 'g-', label='Valor Real')
        pyplot.plot(consolidar_serie(self.trainPredict_v2), 'b-', label='Valor Predito')
        pyplot.xlabel("Tempo (dias)")
        pyplot.ylabel("Valores da cotacao ")
        pyplot.legend()

        pyplot.figure(figsize=(20.5, 3))
        pyplot.plot(consolidar_serie(np.array(self.data['test']['closing (t)'])), 'g-', label='Valor Real')
        pyplot.plot(consolidar_serie(self.testPredict_v2), 'b-', label='Valor Predito')
        pyplot.xlabel("Tempo (dias)")
        pyplot.ylabel("Valores da cotação ")
        pyplot.legend()

    def save_plot_result(self, name):
        """Salva em dois arquivos csv's, os pontos necessários para plotar o resultado obtido ( previsão )"""
        file_name = name

        if not os.path.exists(self.path + file_name):
            os.makedirs(self.path + file_name)

        train_set = DataFrame(data=[consolidar_serie(array(self.data['train']['closing (t)'])),
                                    consolidar_serie(self.trainPredict_v2)]).transpose()

        # Train Set

        train_set_v1 = DataFrame(train_set).rename(columns={0: "Real", 1: "Predito"})
        train_set_v1.index.name = 'index'
        train_set_v1.to_csv(
            path_or_buf=self.path + file_name + '/train.csv')

        # Test Set
        test_set_v1 = DataFrame(data=[consolidar_serie(array(self.data['test']['closing (t)'])),
                                      consolidar_serie(self.testPredict_v2)]).transpose()
        test_set_v2 = pd.DataFrame(test_set_v1).rename(columns={0: "Real", 1: "Predito"})
        test_set_v2.index.name = 'index'
        test_set_v2.to_csv(path_or_buf=self.path + file_name + '/test.csv')
