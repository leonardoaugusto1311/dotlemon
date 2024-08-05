import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Lançamento Pós",
    page_icon="🟢"
)
st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
st.title('POLÍTICAS PÓS') # título
st.info('🟡 Preencha os campos com as informações solicitadas 🟡') # informativo

# Inicializa os valores na sessão
if 'cliente_p2' not in st.session_state:
    st.session_state['cliente_p2'] = 0.0
if 'cliente_m2' not in st.session_state:
    st.session_state['cliente_m2'] = 0.0
if 'comissao_p2' not in st.session_state:
    st.session_state['comissao_p2'] = 0.0
if 'comissao_m2' not in st.session_state:
    st.session_state['comissao_m2'] = 0.0
if 'comissao_g2' not in st.session_state:
    st.session_state['comissao_g2'] = 0.0

# Definindo os inputs com valores inicializados corretamente como float
st.session_state['cliente_p2'] = st.number_input("Cliente P (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_p2']))
st.session_state['cliente_m2'] = st.number_input("Cliente M (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_m2']))
st.session_state['comissao_p2'] = st.number_input("Cliente P (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_p2']))
st.session_state['comissao_m2'] = st.number_input("Cliente M (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_m2']))
st.session_state['comissao_g2'] = st.number_input("Cliente G (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_g2']))

if st.button("Enviar" , key = '1'):
    # Recuperar valores do session_state
    cliente_p2 = st.session_state['cliente_p2']
    cliente_m2 = st.session_state['cliente_m2']
    comissao_p2 = st.session_state['comissao_p2']
    comissao_m2 = st.session_state['comissao_m2']
    comissao_g2 = st.session_state['comissao_g2']

    # Aqui você pode adicionar a lógica para salvar ou processar os valores recebidos
    st.success("Dados enviados com sucesso!")