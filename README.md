
## Modelo Preditivo de Séries Temporais Financeiras utilizando Redes Neurais

* Projeto que tem como objetivo a construção de um sistema capaz de realizar transações no Mercado Financeiro, 
especialmente no Mercado de criptomoedas ou moedas virtuais, no qual, utiliza-se modelos preditivos como uma das 
atividades essênciais e diferenciais do sistema de trading, implementados utilizando Redes Neurais Artificiais.

Data  | Status | Versão
------------- | ------------- |
08/01/2018 | Teste do protótipo Scraping() para coleta de dados | Scraping 1.0
10/01/2018 | Melhoria do job Scraping() para coleta de dados | Scraping 1.1 
15/01/2018 | Inicio da coleta de dados através da primeira versão do Scraping | Scraping 1.1
16/01/2018 | Início da implementação das funções de Pré-processamento de dados

# Observações

Data  | Versão 
------------- | -------------
15/01/2018 | Scraping 1.1 

Versão necessita de um mecanismo multi-thread para captação de dados de diferentes fontes
* * * 

# Table of contents
* Introdução
* Requerimentos 
* Módulos
* Configuração 

# Introdução

## Implementação do Scraping(): 
* Na etapa atual, é realizado uma classe Scraping no qual faz uso dos dados real-time de diversos brokers, 
que fornecem serviços para compra e venda de ativos financeiros e moedas virtuais como o Bitcoin.
O objetivo do Scraping() é coletar os dados minuto à minuto das corretoras para que se possa realizar o que é
denominado na economia de arbitragem.  

Referências: https://pt.wikipedia.org/wiki/Arbitragem_(economia)

# Módulos 

## Módulos necessários: 

* Pymongo
* JSON
* Datetime
* Thread 
* Requests
* Schedule 
* time 
* Abc ( Abstract Base Classes )
* Functools