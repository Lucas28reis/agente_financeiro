import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class BancoCentralData:
    @staticmethod
    def get_interest_rate():
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"
        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
            if data:
                return f"Taxa SELIC atual: {data[0]['valor']}%"
            else:
                return "Taxa SELIC atual: Dados indisponíveis"
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar dados do Banco Central: {e}")
            return "Taxa SELIC atual: Erro ao acessar dados"

    @staticmethod
    def get_exchange_rate():
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados/ultimos/1?formato=json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data:
                return f"Taxa de câmbio atual (USD/BRL): R$ {data[0]['valor']}"
            else:
                return "Taxa de câmbio atual: Dados indisponíveis"
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar dados do Banco Central: {e}")
            return "Taxa de câmbio atual: Erro ao acessar dados"

    @staticmethod
    def get_ipca():
        url = 'https://brasilindicadores.com.br/ipca'
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            card_body_textos = soup.select('.secao-pagina.container .row.justify-content-center.align-items-center .col-6.col-md-4.card-inicial-indicador .card .card-body .card-body-texto')
            
            if len(card_body_textos) > 1:
                card_body_texto = card_body_textos[1]
                ipca_text = card_body_texto.get_text(strip=True)
                return f"IPCA atual: {ipca_text}"
            else:
                return "IPCA atual: Dados insuficientes"
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao acessar dados do Brasil Indicadores: {e}")
            return "IPCA atual: Erro ao acessar dados"