import requests

class BancoCentralData:
    @staticmethod
    def get_interest_rate():
        # Exemplo de URL para obter a taxa SELIC do Banco Central
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1178/dados/ultimos/1?formato=json"
        response = requests.get(url)
        data = response.json()
        return f"Taxa SELIC atual: {data[0]['valor']}%"

    @staticmethod
    def get_exchange_rate():
        # Exemplo de URL para obter a taxa de câmbio do Banco Central
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados/ultimos/1?formato=json"
        response = requests.get(url)
        data = response.json()
        return f"Taxa de câmbio atual (USD/BRL): R$ {data[0]['valor']}"