import abc
import json
from datetime import date, timedelta
from threading import Thread
import requests


class RequestHistorico(Thread):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request_data(self):
        """Assinatura da função que realiza a requisição de dados"""


class MercadoBitcoin(RequestHistorico):
    market = "Mercado Bit Coin"

    def __init__(self, coin, date_request):
        super().__init__()

        self.coin = coin
        self.date_request = date_request
        self.source = "https://www.mercadobitcoin.net/api/" + self.coin + "/day-summary/" + self.date_request
        self.data = {}

    def request_data(self):

        try:
            requisition = requests.get(self.source)
            self.data.update(json.loads(requisition.text))
            self.data.update({"coin": self.coin})

        except requests.exceptions.ConnectionError as error:

            print("<Erro na requisição dos dados> : %s" % error)

        except requests.exceptions.Timeout as error:

            print("<Erro na requisição dos dados> : %s " % error)


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

    @staticmethod
    def get_historico_batch():
        coin_first_date = [{'BTC': date(2013, 6, 12)}, {'LTC': date(2013, 8, 23)}, {'BCH': date(2017, 8, 21)}]

        for item in coin_first_date:
            dinicio = list(item.values())[0]
            dfim = date.today() - timedelta(days=1)
            periodo = dfim - dinicio

            for i in range(periodo.days + 1):
                date_parsing = str(dinicio + timedelta(days=i))
                date_request = date_parsing.replace("-", '/')

                item_request = MercadoBitcoin(coin=list(item.keys())[0], date_request=date_request)
                item_request.request_data()
                print(item_request.data)


coletor = ColetorHistorico(MercadoBitcoin)
coletor.get_historico_batch()
