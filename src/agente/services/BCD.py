import requests
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

