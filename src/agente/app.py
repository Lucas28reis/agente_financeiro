import streamlit as st
from agente import Agent
import json

st.set_page_config(page_title="Agente Financeiro", page_icon="💸")

st.title("💸🤖 - Agente :green[Financeiro]")
st.subheader('',divider='rainbow')

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

def save_feedback(request, response, feedback):
    feedback_data = {
        "request": request,
        "response": response,
        "feedback": feedback
    }
    try:
        with open("feedback.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    data.append(feedback_data)
    with open("feedback.json", "w") as file:
        json.dump(data, file)

api_key = st.text_input('Insira sua chave API Gemini 🔐', type='password')

request = st.text_area("Qual conselho financeiro você gostaria?")
button = st.button("Pedir sugestão", type="primary")
box = st.container(border=True)

with box:
    container = st.empty()
    container.header("Conselho Financeiro")

if button and request and api_key:
    with st.spinner('obtendo conselho financeiro....'):
        agent = Agent(api_key=api_key)
        reset_session_state()
        try:
            advice = agent.get_financial_advice(request)
            if isinstance(advice, dict) and 'financial_advice' in advice:
                response = advice['financial_advice']
                container.write(response)
                
                st.write("Você gostou da resposta?")
                col1, col2 = st.columns([1,1])
                with col1:
                    if st.button("👍"):
                        save_feedback(request, response, "positive")
                        st.success("Obrigado pelo feedback positivo!")
                with col2:
                    if st.button("👎"):
                        save_feedback(request, response, "negative")
                        st.success("Obrigado pelo feedback!")
            else:
                container.write("Resposta inesperada do agente.")
        except Exception as e:
            if "API_KEY_INVALID" in str(e):
                container.write("Erro ao obter conselho financeiro: Chave de API não fornecida ou inválida.")
            else:
                container.write(f"Erro ao obter conselho financeiro: {e}")
