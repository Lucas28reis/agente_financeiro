import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from services.BCD import BancoCentralData 

logging.basicConfig(level=logging.INFO)

class FinancialConsultantTemplate:
    def __init__(self):
        self.template = """"
        Você é um assistente de consultoria financeira que ajuda os usuários com conselhos ou planejamento financeiro.
        Converta a solicitação do usuário em um conselho financeiro detalhado, incluindo orçamento, investimento e gestão de dívidas quando for necessário ou em uma explicação seguindo uma linha lógica.
        Responda sempre o que for solicitado e utilize a técnica "Explique para uma criança de 5 anos".
        Utilize dados atualizados do Banco Central do Brasil para enriquecer suas respostas.
        Utilize a formatação de equações para as respostas com cálculo e letra Calibri como padrão.
        Sua resposta deve ser compreensível, extrovertida, legal e simples, use exemplos práticos e listas para explicar o que foi pedido.
        
        ####
        User: Quanto que eu tenho que ter investido para uma renda mensal de 5 mil reais. Considere a taxa SELIC atual?

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

    def get_financial_advice(self, request, monthly_statement):
        financial_consultant_template = FinancialConsultantTemplate()

        try:
            interest_rate = BancoCentralData.get_interest_rate()
            exchange_rate = BancoCentralData.get_exchange_rate()
        except Exception as e:
            self.logger.error(f"Erro ao obter dados do Banco Central: {e}")
            interest_rate = "Dados da taxa SELIC indisponíveis"
            exchange_rate = "Dados da taxa de câmbio indisponíveis"
        
        formatted_statement = "\n".join([f"{category}: R$ {amount}" for category, amount in monthly_statement.items()])
        enriched_request = f"{request}\n\nFatura Mensal:\n{formatted_statement}\n\nDados atualizados:\n{interest_rate}\n{exchange_rate}"

        parser = LLMChain(
            llm=self.chat_model,
            prompt=financial_consultant_template.prompt_template,
            verbose=self.verbose,
            output_key='financial_advice'
        )

        response = parser.run({"request": enriched_request})
        if isinstance(response, str):
            return {"financial_advice": response}

        self.logger.error(f"Resposta inesperada: {response}")
        raise ValueError(f"A resposta não é uma string conforme esperado.")
