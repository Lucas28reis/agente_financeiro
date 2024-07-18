import requests

class BancoCentralData:
    @staticmethod
    def get_interest_rate():
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados/ultimos/1?formato=json"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro ao obter taxa SELIC: {response.status_code}")
        try:
            data = response.json()
        except ValueError:
            raise Exception("Erro ao decodificar resposta JSON da taxa SELIC.")
        return f"Taxa SELIC atual: {data[0]['valor']}%"

    @staticmethod
    def get_exchange_rate():
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados/ultimos/1?formato=json"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Erro ao obter taxa de câmbio: {response.status_code}")
        try:
            data = response.json()
        except ValueError:
            raise Exception("Erro ao decodificar resposta JSON da taxa de câmbio.")
        return f"Taxa de câmbio atual (USD/BRL): R$ {data[0]['valor']}"
