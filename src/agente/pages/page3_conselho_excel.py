import streamlit as st
from agente import Agent
from config import api_key

agent = Agent(api_key=api_key)

def show_excel_page():
    st.header("Analisar Fatura do Excel")
    excel_file = st.file_uploader("Envie o arquivo Excel", type=["xls", "xlsx"])

    if st.button("Analisar Excel"):
        if excel_file:
            advice_from_excel = agent.analyze_excel(excel_file)
            st.write("Aqui estão as dicas financeiras com base na sua fatura do Excel:")
            st.write(advice_from_excel)
        else:
            st.write("Por favor, envie um arquivo Excel.")
