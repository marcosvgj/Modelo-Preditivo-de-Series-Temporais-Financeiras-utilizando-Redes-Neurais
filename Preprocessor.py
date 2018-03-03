from DatabaseConnection import MongoDB
import pandas as pd
from pandas import DataFrame
from pandas import concat
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# from sklearn.model_selection import GridSearchCV

def parser(data, coin, formatt=None):
    """ Criação de um Pandas Dataframe com as informações contidas no banco não relacional. O método recebe como
    parâmetro uma coleção de objetos JSON e os realoca construindo um Pandas DataFrame para o tipo de moeda
    selecionado. """
    switcher = {'BTC': 0, 'LTC': 1, 'BCH': 2}
    tables = {}
    for item in switcher:
        tables[item] = []
        for cursor in data:
            cursor_dict = cursor['info'][switcher[item]]['ticker']
            itz = pd.Series(cursor_dict, index=cursor_dict.keys())
            tables[item].append(itz)
    if formatt is None:
        return np.array(tables[coin])
    elif formatt == 'pandas':
        return pd.DataFrame(tables[coin])
    elif formatt == 'numpy':
        return np.array(tables[coin])


class Preprocessor:
    def __init__(self):
        print("Start Pre-processor .. ")

    def get_data(self, mkt=None, coin=None):
        """ Recupera os dados do mercado selecionado em formato JSON"""
        db_conn = MongoDB()
        data = db_conn.consultar(materialized_mode=True, market=mkt, coin=coin)
        return data

    def sliding_window_v3(self, data, x_in=1, y_out=1, dropnan=True):

        if type(data) is list:
            n_vars = 1
        else:
            n_vars = data.shape[1]

        df = DataFrame(data)
        cols, names = list(), list()

        # Sequencia corrente de entrada
        for i in range(x_in, 0, -1):
            aux_1 = df.shift(-i)
            cols.append(aux_1['last'])
            names += ['last (t)']

        # Sequencia de saída

        for i in range(1, y_out + 1):
            aux = df.shift(-i)
            cols.append(aux['last'])
            # cols.append(df.shift(-i))
            if i == 1:
                names += ['last (t+1)']
            else:
                names += ['last (t+%d)' % i]

        # Junção dos dados coletados

        agg = concat(cols, axis=1)
        agg.columns = names

        # Remove registros com itens nulos

        if dropnan:
            agg.dropna(inplace=True)
        return agg

    def split_train_test(self, data, percentual_train=0.70):
        tam_treino = int(len(data) * percentual_train)
        treino, teste = data[0:tam_treino], data[tam_treino:len(data)]
        return treino, teste

    def split_in_out_v2(self, data):
        x = data.loc[:, :'vol (t)']
        y = data.loc[:, 'last (t+1)':]

        return x, y

    def to_array(self, data):
        info = np.array(data)
        # Alterar o shape da lista `info.shape`
        info = np.reshape(info, (info.shape[0], 1, info.shape[1]))
        return info

    def normalizacao(self, data):
        scaler = MinMaxScaler(feature_range=(-1, 1))
        data_norm = scaler.fit_transform(data)

        return data_norm, scaler

    def reshape_data(self, data):
        return np.reshape(data, (data.shape[0], 1, data.shape[1]))

    def escala_inversa(self, data, new_data):

        scaler = MinMaxScaler(feature_range=(-1, 1))
        scaler.fit_transform(data)
        unormalized = scaler.inverse_transform(new_data)

        return unormalized


