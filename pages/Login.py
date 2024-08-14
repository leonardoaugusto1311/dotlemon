import streamlit as st
from pymongo import MongoClient

# Configurar a conexão com o MongoDB
client = MongoClient('mongodb+srv://leonardoaugusto199813:August@123@precificacao.axzys.mongodb.net/?retryWrites=true&w=majority&appName=Precificacao')
db = client.precificacao
colecao = db.login

# Função para verificar credenciais
def verificar_credenciais(login, senha):
    usuario = colecao.find_one({"login": login})
    if usuario:
        senha_armazenada = usuario.get("senha")
        return senha_armazenada == senha
    return False

# Criar a interface de login
st.title("Página de Login")

# Campos para o login
login = st.text_input("Login")
senha = st.text_input("Senha", type='password')

if st.button("Entrar"):
    if verificar_credenciais(login, senha):
        st.success("Login bem-sucedido!")
    else:
        st.error("Login ou senha incorretos.")
