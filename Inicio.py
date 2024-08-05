import streamlit as st
from streamlit_option_menu import option_menu
import base64
st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)

# Funções para as páginas
def home_page():
    st.set_page_config(
    page_title="Dot Lemon",
    page_icon="🍋")

    st.title('Primeiros Passos') # titulo
    st.info('🟡Leia o passo a passo com atenção🟡') # informativo

#.\dotlemon\Scripts\activate

# Salvar últimos inputs de dados
