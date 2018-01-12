#Importação das bibliotecas necessárias

import datetime
import json
from threading import Thread
from pymongo import MongoClient
import requests
import schedule
import time
import pandas as pd


class Request(Thread):

    def __init__(self,coin):
        self.coin = coin
        self.source = "https://www.mercadobitcoin.net/api/"+self.coin+"/ticker/"
        self.data = {}

    def requestData(self):
        try:
            requisition = requests.get(self.source)
            self.data[self.coin] = json.loads(requisition.text)['ticker']

        except requests.exceptions.ConnectionError:

            print("<Erro na requisição dos dados - Possível Erro: Numero maximo de tentativas excedido>")

        except requests.exceptions.Timeout:

            print("<Erro na requisição dos dados - Possível Erro: Tempo maximo de requisicao excedido>")


class Coletor:

    def __init__(self):

        """ Moedas utilizadas:
            - BTC - BitCoin
            - LTC - LiteCoin
            - BCH - BitCoin Cash
        """

        self.cryptocurrencies = ['BTC','LTC','BCH']
        self.data = {}
        self.Session = MongoClient('localhost', 27017)
        self.UTC_OFFSET = 2

    def requisitarDados(self):
         iterator  = [Request(item) for item in self.cryptocurrencies]
         current_time = (datetime.datetime.utcnow() - datetime.timedelta(hours=self.UTC_OFFSET)).strftime('%Y-%m-%d %H:%M')
         tickers = []

         for item in iterator:
            item.requestData()
            tickers.append(item.data)

         self.data.update({current_time:tickers})

         print(json.dumps(self.data, indent=4, sort_keys=True))

    def armazenarDados(self):
        "Otimizar através do Mediator"
        db = self.Session['SmartCoinDB'].get_collection('SmartCoin')
        db.insert_one(self.data)
        self.Session.close()

    def recuperarDados(self):

        try:
            db = self.Session['SmartCoinDB'].get_collection('SmartCoin').find()
            print ('\n \f Objetos da coleção - SmartCoin \n \f Frequência de atualização dos dados: 1 minuto \n ')

            for emp in db:
                item = emp[list(emp.keys())[1]]

                print(list(emp.keys())[1] + ":" + json.dumps(item, indent=4, sort_keys=True))
                print('\n')
        except:
            print("Tempo excedido - Tente novamente mais tarde")

    def build_in_memory_database(self):
        """Criação do Database para treinamento em batch do modelo"""
        db_pandas_list = []
        db = self.Session['SmartCoinDB'].get_collection('SmartCoin').find()
        for emp in db:
            horario = emp['BTC']['BTC']['ticker']['date']
            #print("Horário: %s " % datetime.datetime.fromtimestamp(int(horario)).strftime('%Y-%m-%d %H:%M'))
            #print("Horario - ENDED REQUEST :  %s" % emp['BTC']['timestamp'])

            for item in self.Cryptocurrencies:
                #print(emp[item][item]['ticker'])
                db_pandas_list.append(emp[item][item]['ticker'])
            #print('\n')

        return pd.DataFrame(db_pandas_list)

def Job():

    "Inicio do PyMongoDB"
    obj = Coletor()
    obj.requisitarDados()
    obj.armazenarDados()

def Scraping():
    schedule.every(1).minute.do(Job)
    while True:
       schedule.run_pending()
       time.sleep(5)

if __name__ == '__main__':

    a = Coletor()
    a.recuperarDados()















