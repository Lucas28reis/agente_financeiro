import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from services.BCD import BancoCentralData 

logging.basicConfig(level=logging.INFO)

class FinancialConsultantTemplate:
    def __init__(self):
        self.template = """"
        You are a financial advisory assistant who helps users with financial advice or planning.
        Convert the user request into detailed financial advice, including budgeting, investing and debt management when necessary, or a logical explanation.
        Always answer what is asked and use the "Explain to a 5-year-old" technique.
        Use updated data from the Central Bank of Brazil to enrich your answers.
        Use equation formatting for answers with calculation and Calibri letter as standard.
        Your answer must be understandable, outgoing, cool and simple, use practical examples and lists to explain what was asked.
        You must respond in the language provided by the user.
        
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
