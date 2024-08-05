import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="LANÇAMENTOS",
    page_icon="🟢"
)
#st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
st.title('LANÇAMENTOS') # título
st.info('🟡 Preencha os campos com as informações solicitadas 🟡') # informativo

# Inicializa os valores na sessão
if 'projeto_meses' not in st.session_state:
    st.session_state['projeto_meses'] = 0.0
if 'fat_lancamento' not in st.session_state:
    st.session_state['fat_lancamento'] = 0.0
if 'traf' not in st.session_state:
    st.session_state['traf'] = 0.0
if 'plat' not in st.session_state:
    st.session_state['plat'] = 0.0
if 'imp' not in st.session_state:
    st.session_state['imp'] = 0.0

# Definindo os inputs com valores inicializados corretamente como float
st.session_state['projeto_meses'] = st.number_input("Total de Meses do Projeto", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['projeto_meses']))
st.session_state['fat_lancamento'] = st.number_input("Faturamento", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['fat_lancamento']))
st.session_state['traf'] = st.number_input("Trafego %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['traf']))
st.session_state['plat'] = st.number_input("Plataforma %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['plat']))
st.session_state['imp'] = st.number_input("Imposto %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['imp']))

if st.button("Enviar"):
    # Recuperar valores do session_state
    projeto_meses = st.session_state['projeto_meses']
    fat_lancamento = st.session_state['fat_lancamento']
    traf = st.session_state['traf']
    st.session_state['traf_valor'] = round(fat_lancamento * (traf/100), 3)
    traf_valor = st.session_state['traf_valor']
    plat = st.session_state['plat']
    st.session_state['plat_valor'] = round(fat_lancamento * (plat/100), 3)
    plat_valor = st.session_state['plat_valor']
    imp = st.session_state['imp']
    st.session_state['imp_valor'] = round(fat_lancamento * (imp/100), 3)
    imp_valor = st.session_state['imp_valor']
    st.session_state['depesas'] = traf_valor+plat_valor+imp_valor
    despesas = st.session_state['depesas']

    comissao_p = st.session_state['comissao_p']
    cliente_p = st.session_state['cliente_p']
    comissao_m = st.session_state['comissao_m']
    cliente_m = st.session_state['cliente_m']
    comissao_g = st.session_state['comissao_g']
    contribuicao_cliente = st.session_state['contribuicao_cliente']
    aliquota_imposto = st.session_state['aliquota_imposto']



    st.success("Dados enviados com sucesso!")
    st.write(f'Trafego R$: {traf_valor} ')
    st.write(f'Plataforma R$: {plat_valor} ')
    st.write(f'Imposto R$: {imp_valor} ')
    st.write(f'Depesas R$: {despesas} ')
    percentuais_politicas = (traf/100) + (plat/100) + (imp/100)

    if fat_lancamento <= cliente_p:
        faixa1 = (fat_lancamento - despesas) * (comissao_p/100)
        faixa2 = 0 
        faixa3 = 0
        st.write(f'Comissão Faixa 1 R$: {faixa1}')
    else:
        faixa1 = (cliente_p - (cliente_p * (percentuais_politicas)))*(comissao_p/100)
        st.write(f'Comissão Faixa 1 R$: {faixa1}')


#---------------------------------------------------------------------------------------
    depesas_clientep = cliente_p*((traf/100) + (plat/100) + (imp/100))
    depesas_clientem = cliente_m*((traf/100) + (plat/100) + (imp/100))

    

    if fat_lancamento <= cliente_p:
        faixa2 = 0 
        faixa3 = 0
                 
    elif fat_lancamento <= cliente_m : 
       parte1 = fat_lancamento - cliente_p
       subtracao_despesas = despesas-depesas_clientep
       faixa2 = (parte1-subtracao_despesas)*(comissao_m/100)
       st.write(f'Comissão Faixa 2 : R${faixa2}')
    else : 
       
       #st.write(percentuais_politicas)
       faixa3 = 0
       subtracao_faixas = cliente_m-cliente_p
       subtracao_despesas = depesas_clientem-depesas_clientep
       faixa2 = (subtracao_faixas-subtracao_despesas)*(comissao_m/100)
       st.write(f'Comissão Faixa 2 : R${faixa2}')
 #------------------------------------------------------------ 


 # faixa 3   
    if fat_lancamento > cliente_m  : 
        parte1 = fat_lancamento - cliente_m
        subtracao_despesas = despesas-depesas_clientem
        faixa3 = (parte1-subtracao_despesas)*(comissao_g/100)
        st.write(f'Comissão Faixa 3 : R${faixa3}')





    umenosaliquota = 1-(aliquota_imposto/100)
    comissao_recebida = faixa1+faixa2+faixa3
    st.write(f'Recebido a título de comissão R$: {comissao_recebida}')

    #tx_fix_mensal  = round(contribuicao_cliente/umenosaliquota,2)
    #st.write(f'Taxa Fixa Mensal: {tx_fix_mensal}')
    #total_recebido = tx_fix_mensal*projeto_meses+comissao_recebida
    #st.write(f'Total Recebido no Projeto: {total_recebido}')
