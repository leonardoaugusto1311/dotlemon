import streamlit as st

st.set_page_config(
    page_title="Avulsos",
    page_icon="🟢"
)
#st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
st.title('AVULSOS')  # título
st.info('🟡 Preencha os campos com as informações solicitadas 🟡')  # informativo

# Inicializa os valores na sessão, mas apenas se ainda não estiverem definidos
default_value = 0.0
if 'folha_pagamento2' not in st.session_state:
    st.session_state['folha_pagamento2'] = 0.0
if 'folha_pagamento3' not in st.session_state:
    st.session_state['folha_pagamento3'] = 0.0
if 'folha_pagamento4' not in st.session_state:
    st.session_state['folha_pagamento4'] = default_value
if 'folha_pagamento5' not in st.session_state:
    st.session_state['folha_pagamento5'] = default_value
if 'folha_pagamento6' not in st.session_state:
    st.session_state['folha_pagamento6'] = default_value
if 'folha_pagamento7' not in st.session_state:
    st.session_state['folha_pagamento7'] = default_value
if 'folha_pagamento8' not in st.session_state:
    st.session_state['folha_pagamento8'] = default_value
if 'folha_pagamento9' not in st.session_state:
    st.session_state['folha_pagamento9'] = default_value
if 'folha_pagamento10' not in st.session_state:
    st.session_state['folha_pagamento10'] = default_value
if 'folha_pagamento11' not in st.session_state:
    st.session_state['folha_pagamento11'] = default_value
if 'folha_pagamento12' not in st.session_state:
    st.session_state['folha_pagamento12'] = default_value
if 'folha_pagamento13' not in st.session_state:
    st.session_state['folha_pagamento13'] = default_value


# Campos de entrada para os dados financeiros
st.session_state['folha_pagamento2'] = st.number_input("% Reinvestimento", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento2'])
st.session_state['folha_pagamento3'] = st.number_input("% Margem", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento3'])
st.session_state['folha_pagamento4'] = st.number_input("Custo hora Copy", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento4'])
st.session_state['folha_pagamento5'] = st.number_input("Horas Gastas Copy", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento5'])
st.session_state['folha_pagamento6'] = st.number_input("Custo Hora Design", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento6'])
st.session_state['folha_pagamento7'] = st.number_input("Horas Gastas Design", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento7'])
st.session_state['folha_pagamento8'] = st.number_input("Custo Hora Trafego", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento8'])
st.session_state['folha_pagamento9'] = st.number_input("Horas Gastas Trafego", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento9'])
st.session_state['folha_pagamento10'] = st.number_input("Custo Hora Automação", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento10'])
st.session_state['folha_pagamento11'] = st.number_input("Horas Gastas Automação", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento11'])
st.session_state['folha_pagamento12'] = st.number_input("Custo Hora Inbound", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento12'])
st.session_state['folha_pagamento13'] = st.number_input("Horas Gastas Inbound", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento13'])

# Botão de enviar
if st.button("Enviar", key='bt23'):
    # Recuperar valores do session_state
    folha_pagamento6 = st.session_state['folha_pagamento6']
    folha_pagamento7 = st.session_state['folha_pagamento7']
    folha_pagamento2 = st.session_state['folha_pagamento2']
    folha_pagamento3 = st.session_state['folha_pagamento3']
    folha_pagamento4 = st.session_state['folha_pagamento4']
    folha_pagamento5 = st.session_state['folha_pagamento5']
    folha_pagamento8 = st.session_state['folha_pagamento8']
    folha_pagamento9 = st.session_state['folha_pagamento9']
    folha_pagamento10 = st.session_state['folha_pagamento10']
    folha_pagamento11 = st.session_state['folha_pagamento11']
    folha_pagamento12 = st.session_state['folha_pagamento12']
    folha_pagamento13 = st.session_state['folha_pagamento13']
    aliquota_imposto = st.session_state['aliquota_imposto']
    
    total_horass = folha_pagamento13 + folha_pagamento11 + folha_pagamento7 + folha_pagamento9 + folha_pagamento5
    custo_total = (folha_pagamento4 * folha_pagamento5) + (folha_pagamento10 * folha_pagamento11) + (folha_pagamento6 * folha_pagamento7) + (folha_pagamento12 * folha_pagamento13) + (folha_pagamento8 * folha_pagamento9)
    fator_preco = 1 / (1 - ((folha_pagamento2 / 100) + (folha_pagamento3 / 100) + (aliquota_imposto / 100)))
    p_final = custo_total * fator_preco

    st.success("Enviados com sucesso!")
    st.write("### Valores Calculados")
    st.write(f"Total de Horas: {total_horass:.0f}")
    st.write(f"Custo Total: {custo_total:.2f}")
    st.write(f"Fator preço: {fator_preco:.2f}")
    st.write(f"Preço Final: {p_final:.0f}")
