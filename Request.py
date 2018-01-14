"""Importação das bibliotecas necessárias"""

from datetime import timedelta
from datetime import datetime
import json
from threading import Thread
import requests
import schedule
from time import sleep
import abc
from DatabaseConnection import MongoDB
from functools import partial


class Request(Thread):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def request_data(self):
        """Assinatura da função que realiza a requisição de dados"""


class RequestMercadoBitcoin(Request):
    market = "Mercado Bit Coin"

    def __init__(self, coin):

        super().__init__()

        self.coin = coin
        self.source = "https://www.mercadobitcoin.net/api/" + self.coin + "/ticker/"
        self.data = {}

    def request_data(self):

        try:
            requisition = requests.get(self.source)
            self.data.update(json.loads(requisition.text))
            self.data.update({"coin":self.coin})

        except requests.exceptions.ConnectionError as error:

            print("<Erro na requisição dos dados: %s" % error)

        except requests.exceptions.Timeout as error:

            print("<Erro na requisição dos dados> : %s " % error)


class RequestNegocieCoins(Request):

    market = "Negocie Coins"

    def __init__(self, coin):

        super().__init__()

        self.coin = coin
        self.source = "https://broker.negociecoins.com.br/api/v3/" + self.coin + "/ticker"
        self.data = {}

    def request_data(self):

        try:
            requisition = requests.get(self.source)
            self.data.update({"ticker":json.loads(requisition.text)})
            self.data.update({"coin": self.coin})

        except requests.exceptions.ConnectionError as error:

            print("<Erro na requisição dos dados> : %s " % error)

        except requests.exceptions.Timeout as error:

            print("<Erro na requisição dos dados> : %s" % error)


class Coletor:
    cryptocurrencies = ['BTC', 'LTC', 'BCH']

    def __init__(self, request_type):
        self.data = {}
        self.utc_offset = 2
        self.request_type = request_type

    def requisitar_dados(self):
        iterator = [self.request_type(item) for item in self.cryptocurrencies]
        current_time = (datetime.utcnow() - timedelta(hours=self.utc_offset)).strftime(
            '%Y-%m-%d %H:%M')
        tickers = []

        for item in iterator:

            Thread(target=item.request_data()).start()
            tickers.append(item.data)
            self.data.update({current_time: tickers, "market": item.market})

        print(json.dumps(self.data, indent=4, sort_keys=True))


class Scraping:

    def __init__(self):
        """ Coleta automatizada dos dados """
        print("Starting Scraping job ...")

    def engine(self,job):
        schedule.every(1).minute.do(job)
        while True:
            schedule.run_pending()
            sleep(5)


def job_for_all_markets(db_connection):

    """ Facade
        Ressalva: Inicializar ambiente multi-thread para coleta em diferentes mercados"""

    market_requests = Request.__subclasses__()

    for item in market_requests:

        requisition = Coletor(item)
        requisition.requisitar_dados()
        db_connection.armazenar_dados(requisition)


def job_for_only_market(db_connection, market_request):

    """ Facade """

    requisition = Coletor(market_request)
    requisition.requisitar_dados()
    db_connection.armazenar_dados(requisition)


if __name__ == '__main__':
    """ Scraping() """
    db_conn = MongoDB()
    db_conn.iniciar_sessao()

    bot = Scraping()
    bot.engine(partial(job_for_only_market, db_conn, RequestMercadoBitcoin))









