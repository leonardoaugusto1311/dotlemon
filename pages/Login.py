import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Função para baixar e carregar a planilha do OneDrive
def load_data_from_onedrive():
    onedrive_link = "https://api.onedrive.com/v1.0/shares/s!AvctgKBRMfiLgpd9WC1dgiFxTfGrSA/root/content"
    response = requests.get(onedrive_link)
    response.raise_for_status()  # Verifica se o download foi bem-sucedido
    excel_data = BytesIO(response.content)
    df = pd.read_excel(excel_data, engine='openpyxl')  # Certifique-se de especificar o motor correto
    return df

# Função para verificar as credenciais
def validate_credentials(username, password, df):
    # Verifica se o nome de usuário e senha fornecidos estão na planilha
    user_row = df[(df['Username'] == username) & (df['Password'] == password)]
    return not user_row.empty

# Página de login
def main():
    st.title("Login Page")

    # Carregar dados da planilha
    st.write("Carregando dados da planilha...")
    df = load_data_from_onedrive()
    st.write("Dados carregados.")

    # Formulário de login
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
