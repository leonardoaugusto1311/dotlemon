import streamlit as st
import pandas as pd
import requests
from io import BytesIO

def load_data_from_onedrive():
    onedrive_link = "https://api.onedrive.com/v1.0/shares/s!AvctgKBRMfiLgpd9WC1dgiFxTfGrSA/root/content"
    response = requests.get(onedrive_link)
    response.raise_for_status()  # Verifica se o download foi bem-sucedido

    # Verifique se o conteúdo é realmente um arquivo Excel
    content_type = response.headers.get('Content-Type')
    st.write(f"Content-Type: {content_type}")

    excel_data = BytesIO(response.content)
    # Tente detectar o tipo de arquivo
    st.write("Detectando tipo de arquivo...")
    
    try:
        df = pd.read_excel(excel_data)
        st.write("Arquivo carregado com sucesso.")
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None

    return df

def validate_credentials(username, password, df):
    if df is not None:
        user_row = df[(df['Username'] == username) & (df['Password'] == password)]
        return not user_row.empty
    return False

def main():
    st.title("Login Page")

    st.write("Carregando dados da planilha...")
    df = load_data_from_onedrive()
    if df is not None:
        st.write("Dados carregados.")

    with st.form(key='login_form'):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if validate_credentials(username, password, df):
                st.success("Login bem-sucedido!")
            else:
                st.error("Nome de usuário ou senha inválidos.")

if __name__ == "__main__":
    main()
