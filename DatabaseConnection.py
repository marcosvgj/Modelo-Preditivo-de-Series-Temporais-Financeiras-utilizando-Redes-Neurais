#!/usr/bin/python

from pymongo import MongoClient
import datetime

#Intenção: Desacoplar o acesso ao banco de dados da aplicação

class MongoDB:
    def __init__(self,host,port):

        # Default Host
        if(host is None): self.host = 'localhost'
        else: self.host = host

        # Default Port
        if(port is None): self.port = 27017
        else: self.port = port



    def iniciarSessao(self):
        self.Session = MongoClient(self.host, self.port)

    def fecharSessao(self):
        self.Session.close()

    def armazenarDados(self,Coletor):
        db = self.Session['SmartCoinDB'].get_collection(Coletor.RequestType.market)
        db.insert_one(self.data)









