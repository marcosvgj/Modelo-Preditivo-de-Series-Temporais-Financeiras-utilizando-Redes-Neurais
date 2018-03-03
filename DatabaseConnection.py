#!/usr/bin/python

from pymongo import errors, MongoClient
import json


# Intenção: Desacoplar o acesso ao banco de dados da classe Coletor

class MongoDB:
    def __init__(self, host=None, port=None):
        self.session = MongoClient()
        # Default Host
        if host is None:
            self.host = 'ds155268.mlab.com'
        else:
            self.host = host
        # Default Port
        if port is None:
            self.port = 55268
        else:
            self.port = port

    def iniciar_sessao(self):
        self.session = MongoClient(self.host,self.port)
        db = self.session['smartbot_database_tcc']
        db.authenticate('marcosvgj', 'a597179b')

    def fechar_sessao(self):
        self.session.close()

    def armazenar_dados(self, coletor):
        db = self.session['smartbot_database_tcc'].get_collection(coletor.request_type.market)
        try:
            db.insert_one(coletor.data)
            print("Data was successfully inserted in the follow Colletion: %s " % coletor.request_type.market)
        except errors.OperationFailure as error:
            print("Could not apply the operation %s" % error)

    def consultar(self, market=None, coin=None, materialized_mode=False):
        if market is None:
            if coin is None:
                col = self.session['smartbot_database_tcc'].collection_names()
                if materialized_mode is True:
                    """ Retornar todos os dados de todas as coleções em uma lista"""
                    tickers = []
                    for item in col:
                        cursor = self.session['smartbot_database_tcc'].get_collection(item)
                        for items in cursor.find({}).sort('timestamp', 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'], 'market': items['market']}
                            tickers.append(item)
                    return tickers
                else:
                    """ Imprime todos os dados de todas as coleções"""
                    for item in col:
                        cursor = self.session['smartbot_database_tcc'].get_collection(item)
                        for items in cursor.find({}).sort('timestamp', 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'], 'market': items['market']}
                            print(json.dumps(item, indent=4, sort_keys=True))
            else:
                """ Retornar as informações sobre a criptomoeda selecionada de todos os mercados"""
                col = self.session['smartbot_database_tcc'].collection_names()
                switcher = {'BTC': 0, 'LTC': 1, 'BCH': 2}
                if materialized_mode is True:
                    """ Retornar as informações sobre a criptomoeda selecionada de todos os mercados em uma lista"""
                    tickers = []
                    for item in col:
                        cursor = self.session['smartbot_database_tcc'].get_collection(item)
                        for items in cursor.find({}).sort("timestamp", 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                    'market': items['market']}
                            tickers.append(item)
                    return tickers
                else:
                    """ Imprime as informações sobre a criptomoeda selecionada de todos os mercados"""
                    for item in col:
                        cursor = self.session['smartbot_database_tcc'].get_collection(item)
                        for items in cursor.find({}).sort("timestamp", 1):
                            item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                    'market': items['market']}
                            print(json.dumps(item, indent=4, sort_keys=True))
        else:
            if coin is None:
                "Retornar todas as informações sobre todas as criptomoedas do mercado selecionado"
                cursor = self.session['smartbot_database_tcc'].get_collection(market)
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
                    cursor = self.session['smartbot_database_tcc'].get_collection(market)
                    switcher = {'BTC': 0, 'LTC': 1, 'BCH': 2}
                    for items in cursor.find({}).sort('timestamp', 1):
                        item = {"timestamp": items['timestamp'], 'info': items['info'][switcher[coin]],
                                'market': items['market']}
                        print(json.dumps(item, indent=4, sort_keys=True))

    def limpar_collections(self, collection):
        """Dropa todo conteúdo referente a uma collection"""
        self.session['smartbot_database_tcc'].get_collection(collection).drop()
