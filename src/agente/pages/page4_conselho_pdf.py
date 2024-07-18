import streamlit as st
from agente import Agent
from config import api_key

agent = Agent(api_key=api_key)

def show_pdf_page():
    st.header("Analisar Fatura do PDF")
    pdf_file = st.file_uploader("Envie o arquivo PDF", type="pdf")

    if st.button("Analisar PDF"):
        if pdf_file:
            advice_from_pdf = agent.analyze_pdf(pdf_file)
            st.write("Aqui estão as dicas financeiras com base na sua fatura do PDF:")
            st.write(advice_from_pdf)
        else:
            st.write("Por favor, envie um arquivo PDF.")
