import streamlit as st
from agente import Agent
from config import api_key

st.set_page_config(page_title="Consultor Financeiro", page_icon="💸")

st.title("Consultor Financeiro")

agent = Agent(api_key=api_key)

def initialize_session_state():
    if "center" not in st.session_state:
        st.session_state.center = [48.9, 2.4]
    if "zoom" not in st.session_state:
        st.session_state.zoom = 10
    if "marker" not in st.session_state:
        st.session_state.marker = []

def reset_session_state():
    for key in st.session_state.keys():
        if key in ["center", "zoom"]:
            continue
        del st.session_state[key]
    initialize_session_state()

request = st.text_area("Qual conselho financeiro você gostaria?")
button = st.button("Pedir sugestão")
box = st.container()
with box:
    container = st.empty()
    container.header("Conselho Financeiro")

if button and request:
    reset_session_state()
    try:
        advice = agent.get_financial_advice(request, {"Outros": 0})
        if isinstance(advice, dict) and 'financial_advice' in advice:
            container.write(advice['financial_advice'])
        else:
            container.write("Resposta inesperada do agente.")
    except Exception as e:
        container.write(f"Erro ao obter conselho financeiro: {e}")

