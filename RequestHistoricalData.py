from datetime import date
from datetime import timedelta
import json
from threading import Thread
import requests
import abc
from DatabaseConnection import MongoDB
from pymongo import errors


class RequestHistorico(Thread):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request_data(self):
        """Assinatura da função que realiza a requisicão de dados"""


class MercadoBitcoin(RequestHistorico):
    market = "Mercado Bit Coin - testing"

    def __init__(self, coin, date_request):
        super().__init__()

        self.coin = coin
        self.date_request = date_request
        self.source = "https://www.mercadobitcoin.net/api/" + self.coin + \
                      "/day-summary/" + self.date_request
        self.data = {}

    def request_data(self):

        try:
            requisition = requests.get(self.source)
            self.data.update(json.loads(requisition.text))
            self.data.update({"coin": self.coin})

        except requests.exceptions.ConnectionError as error:

            print("<Erro na requisicao dos dados> : %s" % error)

        except requests.exceptions.Timeout as error:

            print("<Erro na requisicao dos dados> : %s " % error)


class ColetorHistorico:
    cryptocurrencies = ['BTC', 'LTC', 'BCH']

    def __init__(self, request_type):
        self.data = {}
        self.utc_offset = 2
        self.request_type = request_type

    def get_historico(self, dinicio=None):
        if dinicio is None:
            dinicio = date(2014, 1, 1)

        dfim = date.today() - timedelta(days=1)
        periodo = dfim - dinicio

        for i in range(periodo.days + 1):
            date_parsing = str(dinicio + timedelta(days=i))
            date_request = date_parsing.replace("-", '/')

            iterator = [self.request_type(item, date_request) for item in self.cryptocurrencies]
            for item in iterator:
                item.request_data()

                print(item.data)


class Scraping:
    def __init__(self, db_conn):
        """Coleta dos dados"""
        print("Starting Scraping job ...")
        self.db_conn = db_conn
        self.historical_data = []

    def get_historico_batch(self):

        coin_first_date = [{'BTC': date(2018, 4, 3)},  # \
                           # {'LTC': date(2013, 8, 23)},\
                           # {'BCH': date(2017, 8, 21)}
                           ]

        for item in coin_first_date:
            dinicio = list(item.values())[0]
            dfim = date.today() - timedelta(days=1)
            periodo = dfim - dinicio

            for i in range(periodo.days + 1):
                date_parsing = str(dinicio + timedelta(days=i))
                date_request = date_parsing.replace("-", '/')

                item_request = MercadoBitcoin(coin=list(item.keys())[0], date_request=date_request)
                item_request.request_data()
                self.historical_data.append(item_request.data)
                print(json.dumps(item_request.data, indent=4, sort_keys=True))

    def armazenar_dados(self):
        db = self.db_conn.session['smartbot_database_tcc'].get_collection(MercadoBitcoin.market)

        for item in self.historical_data:
            try:
                db.insert_one(item)
                print("Data was successfully inserted in the follow \
                Colletion: %s " % MercadoBitcoin.market)
            except errors.OperationFailure as error:
                print("Could not apply the \
                operation %s" % error)


if __name__ == '__main__':
    db_connection = MongoDB()
    db_connection.iniciar_sessao()

    coletor_historico = Scraping(db_connection)
    coletor_historico.get_historico_batch()
    coletor_historico.armazenar_dados()
