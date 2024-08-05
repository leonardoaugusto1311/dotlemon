import streamlit as st
import pandas as pd
import base64

st.set_page_config(
    page_title="Pós",
    page_icon="🟢"
)
#st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
st.title('Pós') # título
st.info('🟡 Preencha os campos com as informações solicitadas 🟡') # informativo

# Inicializa os valores na sessão
if 'projeto_meses_pos' not in st.session_state:
    st.session_state['projeto_meses_pos'] = 0.0
if 'fat_lancamento_pos' not in st.session_state:
    st.session_state['fat_lancamento_pos'] = 0.0
if 'traf_pos' not in st.session_state:
    st.session_state['traf_pos'] = 0.0
if 'plat_pos' not in st.session_state:
    st.session_state['plat_pos'] = 0.0
if 'imp_pos' not in st.session_state:
    st.session_state['imp_pos'] = 0.0

# Definindo os inputs com valores inicializados corretamente como float
st.session_state['projeto_meses_pos'] = st.number_input("Total de Meses do Projeto", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['projeto_meses_pos']))
st.session_state['fat_lancamento_pos'] = st.number_input("Faturamento", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['fat_lancamento_pos']))
st.session_state['traf_pos'] = st.number_input("Trafego %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['traf_pos']))
st.session_state['plat_pos'] = st.number_input("Plataforma %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['plat_pos']))
st.session_state['imp_pos'] = st.number_input("Imposto %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['imp_pos']))

if st.button("Enviar"):
    # Recuperar valores do session_state
    projeto_meses_pos = st.session_state['projeto_meses_pos']
    fat_lancamento_pos = st.session_state['fat_lancamento_pos']
    traf_pos = st.session_state['traf_pos']
    st.session_state['traf_pos_valor'] = round(fat_lancamento_pos * (traf_pos/100), 3)
    traf_pos_valor = st.session_state['traf_pos_valor']
    plat_pos = st.session_state['plat_pos']
    st.session_state['plat_pos_valor'] = round(fat_lancamento_pos * (plat_pos/100), 3)
    plat_pos_valor = st.session_state['plat_pos_valor']
    imp_pos = st.session_state['imp_pos']
    st.session_state['imp_valor'] = round(fat_lancamento_pos * (imp_pos/100), 3)
    imp_valor = st.session_state['imp_valor']
    st.session_state['despesas_Pos'] = traf_pos_valor+plat_pos_valor+imp_valor
    despesas_Pos = st.session_state['despesas_Pos']

    comissao_p2 = st.session_state['comissao_p2']
    cliente_p2 = st.session_state['cliente_p2']
    comissao_p2 = st.session_state['comissao_p2']
    cliente_p2 = st.session_state['cliente_p2']
    comissao_g2 = st.session_state['comissao_g2']
    contribuicao_cliente = st.session_state['contribuicao_cliente']
    aliquota_imposto = st.session_state['aliquota_imposto']
    cliente_m2 = st.session_state['cliente_m2']
    comissao_m2 = st.session_state['comissao_m2']


    st.success("Dados enviados com sucesso!")
    st.write(f'Tráfego R$: {traf_pos_valor} ')
    st.write(f'Plataforma R$: {plat_pos_valor} ')
    st.write(f'Imposto R$: {imp_valor} ')
    st.write(f'Despesas: {despesas_Pos} ')

    if fat_lancamento_pos <= cliente_p2:
        faixa1 = (fat_lancamento_pos - despesas_Pos) * (comissao_p2/100)
        
        st.write(f'Comissão Faixa 1 R$: {faixa1}')
    else:
        faixa1 = (cliente_p2 - (cliente_p2 * ((traf_pos/100) + (plat_pos/100) + (imp_pos/100))))*(comissao_p2/100)
        st.write(f'Comissão Faixa 1 R$: {faixa1}')
#---------------------------------------------------------------------------------------
    if fat_lancamento_pos <= cliente_p2:
        faixa2 = 0
        st.write(f"Comissão Faixa 2 R$: {0}")
                 
    elif fat_lancamento_pos <= comissao_m2 : 
       faixa2 = (((fat_lancamento_pos-cliente_p2) - (despesas_Pos - (cliente_p2*((traf_pos/100) + (plat_pos/100) + (imp_pos /100)))))*(comissao_m2/100) )  
       st.write(f' Comissão Faixa 2 R$: {faixa2}')
    
    else : 
       faixa2 = (cliente_m2-cliente_p2+imp_valor-(cliente_m2*((traf_pos/100) + (plat_pos/100) + (imp_pos /100))))*(comissao_g2/100)
       #st.write((cliente_m-cliente_p+imp_valor-(cliente_m*((traf/100) + (plat/100) + (imp /100))))*(comissao_g/100))
       st.write(f"Comissão Faixa 2 R$: {faixa2}")
       #st.write((traf/100) + (plat/100) + (imp /100))
 #------------------------------------------------------------ 
 # faixa 3   
    if fat_lancamento_pos > cliente_m2  : 
        faixa3 = ((fat_lancamento_pos-cliente_m2)-(despesas_Pos - (cliente_m2*((traf_pos/100) + (plat_pos/100) + (imp_pos /100)))))*(comissao_g2/100)   
        st.write(f'Comissão Faixa 3 R$: {faixa3}')   
    else : 
        faixa3 = 0           
        st.write(f'Comissão Faixa 3 R$: {faixa3}')   
    comissao_recebida_pos = faixa1+faixa2+faixa3
    st.write(f'Recebido a título de comissão R$: {comissao_recebida_pos}')
    tx_fix_mensal_pos  = round(contribuicao_cliente/(1-(aliquota_imposto/100)),2)
    st.write(f'Taxa Fixa Mensal: {tx_fix_mensal_pos}')
    total_recebido_pos = tx_fix_mensal_pos*projeto_meses_pos+comissao_recebida_pos
    st.write(f'Total Recebido no Projeto: {total_recebido_pos}')