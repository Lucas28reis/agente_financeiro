import streamlit as st
from agente import Agent
from config import api_key

def show_sheets_page():
    agent = Agent(api_key=api_key)
    
    st.header("Analisar Fatura do Google Sheets")
    sheet_id = st.text_input("ID da Planilha do Google Sheets")
    range_name = st.text_input("Intervalo da Planilha (por exemplo, Sheet1!A1:B10)")
    credentials_json = st.file_uploader("Credenciais JSON do Google Cloud", type="json")

    if st.button("Analisar Google Sheets"):
        if sheet_id and range_name and credentials_json:
            credentials_json = credentials_json.read()
            advice_from_sheets = agent.analyze_google_sheet(sheet_id, range_name, credentials_json)
            st.write("Aqui estão as dicas financeiras com base na sua fatura do Google Sheets:")
            st.write(advice_from_sheets)
        else:
            st.write("Por favor, preencha todos os campos e envie as credenciais JSON.")
