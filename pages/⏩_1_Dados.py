import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Dados",
    page_icon="🟢"
)
st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
st.title('Dados') # titulo
st.info('🟡 Preencha os campos com as informações solicitadas 🟡') # informativo


# Inicializa os valores na sessão
if 'folha_pagamento' not in st.session_state:
    st.session_state['folha_pagamento'] = 0.0
if 'despesas_operacionais' not in st.session_state:
    st.session_state['despesas_operacionais'] = 0.0
if 'despesas_administrativas' not in st.session_state:
    st.session_state['despesas_administrativas'] = 0.0
if 'impostos_pagos' not in st.session_state:
    st.session_state['impostos_pagos'] = 0.0
if 'faturamento' not in st.session_state:
    st.session_state['faturamento'] = 0.0
if 'clientes_medios' not in st.session_state:
    st.session_state['clientes_medios'] = 0

# Campos de entrada para os  financeiros
st.session_state['folha_pagamento'] = st.number_input("Gastos com Folha de Pagamento (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento'])
st.session_state['despesas_operacionais'] = st.number_input("Despesas Operacionais (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['despesas_operacionais'])
st.session_state['despesas_administrativas'] = st.number_input("Despesas Administrativas (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['despesas_administrativas'])
st.session_state['impostos_pagos'] = st.number_input("Impostos Pagos (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['impostos_pagos'])
st.session_state['faturamento'] = st.number_input("Faturamento (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['faturamento'])
st.session_state['clientes_medios'] = st.number_input("Quantidade média de Clientes (Mês):", min_value=0, step=1, format="%d", value=st.session_state['clientes_medios'])

# Botão de enviar
if st.button("Enviar"):
    # Recuperar valores do session_state
    faturamento = st.session_state['faturamento']
    clientes_medios = st.session_state['clientes_medios']
    folha_pagamento = st.session_state['folha_pagamento']
    despesas_operacionais = st.session_state['despesas_operacionais']
    despesas_administrativas = st.session_state['despesas_administrativas']
    impostos_pagos = st.session_state['impostos_pagos']

    # Verificação se os valores necessários foram inseridos
    if faturamento > 0 and clientes_medios > 0 and folha_pagamento > 0 and despesas_operacionais > 0 and despesas_administrativas > 0 and impostos_pagos > 0:
        # Cálculo das variáveis
        st.session_state['aliquota_imposto'] = round(impostos_pagos / faturamento, 2) * 100
        aliquota_imposto = st.session_state['aliquota_imposto']
        st.session_state['custo_mensal_coberto'] = round((folha_pagamento + despesas_operacionais + despesas_administrativas) / 12, 2)
        custo_mensal_coberto = st.session_state['custo_mensal_coberto']
        st.session_state['contribuicao_cliente'] = round(custo_mensal_coberto / clientes_medios, 2)
        contribuicao_cliente = st.session_state['contribuicao_cliente']
        despesa_receita = round(custo_mensal_coberto / (faturamento / 12), 3) * 100

        # Exibição das variáveis calculadas
        st.success(" Valores enviados com sucesso!")
        st.write("### Valores Calculados")
        st.write(f"Alíquota de Imposto: {aliquota_imposto:.0f}%")
        st.write(f"Custo Mensal Coberto: R$ {custo_mensal_coberto:.2f}")
        st.write(f"Contribuição por Cliente: R$ {contribuicao_cliente:.2f}")
        st.write(f"Despesa/Receita: {despesa_receita:.0f}%")
    else:
        st.warning("Insira todos os campos.")

