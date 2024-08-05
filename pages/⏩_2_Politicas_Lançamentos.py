import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Políticas",
    page_icon="🟢"
)
st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
st.title('POLÍTICAS LANÇAMENTOS') # título
st.info('🟡 Preencha os campos com as informações solicitadas 🟡') # informativo

# Inicializa os valores na sessão
if 'cliente_p' not in st.session_state:
    st.session_state['cliente_p'] = 0.0
if 'cliente_m' not in st.session_state:
    st.session_state['cliente_m'] = 0.0
if 'comissao_p' not in st.session_state:
    st.session_state['comissao_p'] = 0.0
if 'comissao_m' not in st.session_state:
    st.session_state['comissao_m'] = 0.0
if 'comissao_g' not in st.session_state:
    st.session_state['comissao_g'] = 0.0

# Definindo os inputs com valores inicializados corretamente como float
st.session_state['cliente_p'] = st.number_input("Cliente P (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_p']))
st.session_state['cliente_m'] = st.number_input("Cliente M (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_m']))
st.session_state['comissao_p'] = st.number_input("Cliente P (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_p']))
st.session_state['comissao_m'] = st.number_input("Cliente M (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_m']))
st.session_state['comissao_g'] = st.number_input("Cliente G (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_g']))

if st.button("Enviar" , key = '1'):
    # Recuperar valores do session_state
    cliente_p = st.session_state['cliente_p']
    cliente_m = st.session_state['cliente_m']
    comissao_p = st.session_state['comissao_p']
    comissao_m = st.session_state['comissao_m']
    comissao_g = st.session_state['comissao_g']

    # Aqui você pode adicionar a lógica para salvar ou processar os valores recebidos
    st.success("Dados enviados com sucesso!")


# Retirar o Cliente G (Faturamento Max)