#!/usr/bin/python

from pymongo import errors, MongoClient
import json


# Intenção: Desacoplar o acesso ao banco de dados da classe Coletor

class MongoDB:
    def __init__(self):
        self.session = None
        self.host = 'ds155268.mlab.com'
        self.port = 55268
        self.user = 'marcosvgj'
        self.user_password = 'a597179b'
        self.collection = 'smartbot_database_tcc'

    def iniciar_sessao(self):
        self.session = MongoClient(self.host, self.port)
        db = self.session[self.collection]
        db.authenticate(self.user, self.user_password)
        return db

    def fechar_sessao(self):
        self.session.close()

    def armazenar_dados(self, coletor):
        db = self.session[self.collection].get_collection(coletor.request_type.market)
        try:
            db.insert_one(coletor.data)
            print("Data was successfully inserted in the follow Colletion: %s " % coletor.request_type.market)
        except errors.OperationFailure as error:
            print("Could not apply the operation %s" % error)

    def consultar(self, market=None, coin=None, materialized_mode=False):
        if market is None:
            if coin is None:
                col = self.session[self.collection].collection_names()
                if materialized_mode is True:
                    """ Retornar todos os dados de todas as coleções em uma lista"""
                    tickers = []
                    for item in col:
                        cursor = self.session[self.collection].get_collection(item)
                        for items in cursor.find({}).sort('timestamp', 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'], 'market': items['market']}
                            tickers.append(item)
                    return tickers
                else:
                    """ Imprime todos os dados de todas as coleções"""
                    for item in col:
                        cursor = self.session[self.collection].get_collection(item)
                        for items in cursor.find({}).sort('timestamp', 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'], 'market': items['market']}
                            print(json.dumps(item, indent=4, sort_keys=True))
            else:
                """ Retornar as informações sobre a criptomoeda selecionada de todos os mercados"""
                col = self.session[self.collection].collection_names()
                switcher = {'BTC': 0, 'LTC': 1, 'BCH': 2}
                if materialized_mode is True:
                    """ Retornar as informações sobre a criptomoeda selecionada de todos os mercados em uma lista"""
                    tickers = []
                    for item in col:
                        cursor = self.session[self.collection].get_collection(item)
                        for items in cursor.find({}).sort("timestamp", 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                    'market': items['market']}
                            tickers.append(item)
                    return tickers
                else:
                    """ Imprime as informações sobre a criptomoeda selecionada de todos os mercados"""
                    for item in col:
                        cursor = self.session[self.collection].get_collection(item)
                        for items in cursor.find({}).sort("timestamp", 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                    'market': items['market']}
                            print(json.dumps(item, indent=4, sort_keys=True))
        else:
            if coin is None:
                "Retornar todas as informações sobre todas as criptomoedas do mercado selecionado"
                cursor = self.session[self.collection].get_collection(market)
                if materialized_mode is True:
                    "Retornar todas as informações sobre todas as criptomoedas do mercado selecionado em uma lista"
                    tickers = []
                    for items in cursor.find({}).sort("timestamp", 1):
                        item = {"timestamp": items['timestamp'], 'info': items['info'], 'market': items['market']}
                        tickers.append(item)
                    return tickers
                else:
                    "Imprime todas as informações sobre todas as criptomoedas do mercado selecionado"
                    for items in cursor.find({}).sort("timestamp", 1):
                        item = {"timestamp": items['timestamp'], 'info': items['info'], 'market': items['market']}
                        print(json.dumps(item, indent=4, sort_keys=True))
            else:
                if materialized_mode is True:
                    """ Retornar as informações sobre a criptomoeda selecionada do mercado selecionado em uma lista"""
                    cursor = self.session['smartbot_database_tcc'].get_collection(market)
                    switcher = {'BTC': 0, 'LTC': 1, 'BCH': 2}
                    tickers = []
                    for items in cursor.find({}).sort('timestamp', 1):
                        item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                'market': items['market']}
                        tickers.append(item)
                    return tickers
                else:
                    """ Imprime as informações sobre a criptomoeda selecionada do mercado selecionado em uma lista"""
                    cursor = self.session[self.collection].get_collection(market)
                    switcher = {'BTC': 0, 'LTC': 1, 'BCH': 2}
                    for items in cursor.find({}).sort('timestamp', 1):
                        item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                'market': items['market']}
                        print(json.dumps(item, indent=4, sort_keys=True))

    def limpar_collections(self, collection):
        """Dropa todo conteúdo referente a uma collection"""
        self.session[self.collection].get_collection(collection).drop()
