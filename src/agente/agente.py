import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from services.BCD import BancoCentralData 

logging.basicConfig(level=logging.INFO)

class FinancialConsultantTemplate:
    def __init__(self):
        self.template = """"
        Você é um assistente de consultoria financeira que ajuda os usuários com consultoria ou planejamento financeiro.
        Converta a solicitação do usuário em aconselhamento financeiro detalhado, incluindo orçamento, investimento e gestão de dívidas quando necessário, ou em uma explicação lógica.
        utilize raciocínio em cadeia de pensamento(CoT), gere um conjunto diversificado de caminhos de raciocínio e selecione a saída mais consistente para atender ao usuário.
        Utilize dados atualizados como taxa SELIC, Dólar e IPCA. do Banco Central do Brasil para enriquecer suas respostas.
        Use a formatação de equações em containers para respostas com cálculo e letra Calibri como padrão.
        Sua resposta deve ser compreensível, extrovertida, bacana e simples, utilize exemplos práticos formatados e listas para explicar o que foi perguntado.
        Você deve responder no idioma fornecido pelo usuário.
        Responda somente o que lhe for perguntado e nada mais.

        ####
        User: O que eu tenho que fazer para ...... 

        Agent: Vamos lá. Aqui estão algumas dicas que podem te ajudar:
        {request}
        ####
        """

        self.prompt_template = PromptTemplate.from_template(self.template)
class Agent:
    def __init__(self, api_key, model_name='gemini-pro', verbose=False, temperature=0):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.verbose = verbose
        self.temperature = temperature
        self._api_key = api_key

        self.chat_model = ChatGoogleGenerativeAI(model=model_name, google_api_key=self._api_key)

    def get_financial_advice(self, request):
        financial_consultant_template = FinancialConsultantTemplate()

        try:
            interest_rate = BancoCentralData.get_interest_rate()
            exchange_rate = BancoCentralData.get_exchange_rate()
            ipca = BancoCentralData.get_ipca()
        except Exception as e:
            self.logger.error(f"Erro ao obter dados do Banco Central: {e}")
            interest_rate = "Dados da taxa SELIC indisponíveis"
            exchange_rate = "Dados da taxa de câmbio indisponíveis"
            ipca = "Dados do IPCA indisponíveis"
        
        enriched_request = (
            f"{request}\n\nDados atualizados:\n{interest_rate}\n{exchange_rate}\n"
            f"{ipca}"
        )

        parser = LLMChain(
            llm=self.chat_model,
            prompt=financial_consultant_template.prompt_template,
            verbose=self.verbose,
            output_key='financial_advice'
        )

        try:
            response = parser.run({"request": enriched_request})
            if isinstance(response, str):
                return {"financial_advice": response}

            self.logger.error(f"Resposta inesperada: {response}")
            raise ValueError("A resposta não é uma string conforme esperado.")
        except Exception as e:
            self.logger.error(f"Erro ao processar o pedido: {e}")
            raise
