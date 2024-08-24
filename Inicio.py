import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus

# Codificar a senha para incluir na URI
username = "leonardoaugusto199813"
password = quote_plus("August@123")

# Configurar a conexão com o MongoDB
client = MongoClient(f'mongodb+srv://{username}:{password}@precificacao.axzys.mongodb.net/?retryWrites=true&w=majority&appName=Precificacao')
db = client.precificacao
colecao = db.login

# Função para verificar credenciais
def verificar_credenciais(login, senha):
    usuario = colecao.find_one({"login": login})
    if usuario:
        senha_armazenada = usuario.get("senha")
        tipo_usuario = usuario.get("tipo")
        return senha_armazenada == senha , tipo_usuario

    return False , None

# Página Login
def pagina_login():
    st.title("Página de Login")

    # Campos para o login
    login = st.text_input("Login")
    senha = st.text_input("Senha", type='password')

    if st.button("Entrar"):
        login_valido, tipo_usuario = verificar_credenciais(login, senha)
        if login_valido:
            st.session_state['login'] = True
            st.session_state['tipo_usuario'] = tipo_usuario  # Armazenar o tipo de usuário na sessão
            st.success("Login bem-sucedido!")
            st.experimental_rerun()  # Recarregar para refletir o estado de login
        else:
            st.error("Login ou senha incorretos.")


# Função para exibir a segunda página (Dados)
def pagina_dados():
    st.title('Dados')  # Título da página
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')  # Informativo

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

    # Campos de entrada para os dados financeiros
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
            st.session_state['aliquota_imposto'] = (impostos_pagos / faturamento) * 100
            aliquota_imposto = st.session_state['aliquota_imposto']
            st.session_state['custo_mensal_coberto'] = round((folha_pagamento + despesas_operacionais + despesas_administrativas) / 12, 2)
            custo_mensal_coberto = st.session_state['custo_mensal_coberto']
            st.session_state['contribuicao_cliente'] = round(custo_mensal_coberto / clientes_medios, 2)
            contribuicao_cliente = st.session_state['contribuicao_cliente']
            despesa_receita = round(custo_mensal_coberto / (faturamento / 12), 3) * 100

            # Exibição das variáveis calculadas
            st.success("Valores enviados com sucesso!")
            st.write("### Valores Calculados")
            st.write(f"Alíquota de Imposto: {aliquota_imposto:.0f}%")
            st.write(f"Custo Mensal Coberto: R$ {custo_mensal_coberto:.2f}")
            st.write(f"Contribuição por Cliente: R$ {contribuicao_cliente:.2f}")
            st.write(f"Despesa/Receita: {despesa_receita:.0f}%")
        else:
            st.warning("Insira todos os campos.")


# Exemplo de uma outra página fictícia
def pagina_lancamentos():
    #st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
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


def pagina_policas_pos():
    #st.image(r"C:\Users\user\Desktop\Projetos\Dot_lemon\dotlemon logo.png", width=200)
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

def pagina_avulsos():
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

def pagina_lancamentos_politicas():
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
        else : 
            faixa3 = 0




        umenosaliquota = 1-(aliquota_imposto/100)
        comissao_recebida = faixa1+faixa2+faixa3
        st.write(f'Recebido a título de comissão R$: {comissao_recebida}')

        tx_fix_mensal  = round(contribuicao_cliente/umenosaliquota,2)
        st.write(f'Taxa Fixa Mensal: {tx_fix_mensal}')
        total_recebido = tx_fix_mensal*projeto_meses+comissao_recebida
        st.write(f'Total Recebido no Projeto: R${round(total_recebido,2)}')


def pagina_pos_politicas():
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
        st.write(f'Despesas R$: {despesas_Pos} ')

        percentuais_politicas = (traf_pos/100) + (plat_pos/100) + (imp_pos/100)

        if fat_lancamento_pos <= cliente_p2:
            faixa1 = (fat_lancamento_pos - despesas_Pos) * (comissao_p2/100)
            faixa2 = 0 
            faixa3 = 0
            st.write(f'Comissão Faixa 1 R$: {faixa1}')
        else:
            faixa1 = (cliente_p2 - (cliente_p2 * (percentuais_politicas)))*(comissao_p2/100)
            st.write(f'Comissão Faixa 1 R$: {faixa1}')


    #---------------------------------------------------------------------------------------
        depesas_clientep = cliente_p2*((traf_pos/100) + (plat_pos/100) + (imp_pos/100))
        depesas_clientem = cliente_m2*((traf_pos/100) + (plat_pos/100) + (imp_pos/100))

        

        if fat_lancamento_pos <= cliente_p2:
            faixa2 = 0 
            faixa3 = 0
                    
        elif fat_lancamento_pos <= cliente_m2 : 
            parte1 = fat_lancamento_pos - cliente_p2
            subtracao_despesas = despesas_Pos-depesas_clientep
            faixa2 = (parte1-subtracao_despesas)*(comissao_m2/100)
            st.write(f'Comissão Faixa 2 : R${faixa2}')
        else : 
        
        #st.write(percentuais_politicas)
            faixa3 = 0
            subtracao_faixas = cliente_m2-cliente_p2
            subtracao_despesas = depesas_clientem-depesas_clientep
            faixa2 = (subtracao_faixas-subtracao_despesas)*(comissao_m2/100)
        st.write(f'Comissão Faixa 2 : R${faixa2}')
    #------------------------------------------------------------ 


    # faixa 3   
        if fat_lancamento_pos > cliente_m2 : 
            parte1 = fat_lancamento_pos - cliente_m2
            subtracao_despesas = despesas_Pos-depesas_clientem
            faixa3 = (parte1-subtracao_despesas)*(comissao_g2/100)
            st.write(f'Comissão Faixa 3 : R${faixa3}')
        else : 
            faixa3 = 0




        umenosaliquota = 1-(aliquota_imposto/100)
        comissao_recebida = faixa1+faixa2+faixa3
        st.write(f'Recebido a título de comissão R$: {comissao_recebida}')

        tx_fix_mensal  = round(contribuicao_cliente/umenosaliquota,2)
        st.write(f'Taxa Fixa Mensal: {tx_fix_mensal}')
        total_recebido = tx_fix_mensal*projeto_meses_pos+comissao_recebida
        st.write(f'Total Recebido no Projeto: R${round(total_recebido,2)}')

# Função principal para gerenciar a navegação

    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['tipo_usuario'] = None  # Inicializar tipo_usuario na sessão

    if st.session_state['login']:
        # Verifica o tipo de usuário antes de exibir o menu
        if st.session_state['tipo_usuario'] == 1:
            # Menu de navegação após login bem-sucedido
            pagina_selecionada = st.sidebar.selectbox("Selecione a Página", ["Dados", "Políticas Lançamentos","Políticas Pós","Avulsos","Lançamentos","Pós"])
            
            if pagina_selecionada == "Dados":
                pagina_dados()
            elif pagina_selecionada == "Políticas Lançamentos":
                pagina_lancamentos()
            elif pagina_selecionada == "Políticas Pós":
                pagina_policas_pos()
            elif pagina_selecionada == "Avulsos":
                pagina_avulsos()
            elif pagina_selecionada == "Lançamentos":
                pagina_lancamentos_politicas()
            elif pagina_selecionada == "Pós":
                pagina_policas_pos()
        else:
            if pagina_selecionada == "Avulsos":
                pagina_avulsos()
            elif pagina_selecionada == "Lançamentos":
                pagina_lancamentos_politicas()
            elif pagina_selecionada == "Pós":
                pagina_policas_pos()
    else:
        pagina_login()

def main():
    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['tipo_usuario'] = None  # Inicializar tipo_usuario na sessão

    if st.session_state['login']:
        # Menu de navegação após login bem-sucedido
        if st.session_state['tipo_usuario'] == 1:
            # Menu completo para tipo_usuario == 1
            opcoes = ["Dados", "Políticas Lançamentos", "Políticas Pós", "Avulsos", "Lançamentos", "Pós"]
        else:
            # Menu limitado para outros tipos de usuários
            opcoes = ["Avulsos", "Lançamentos", "Pós"]
        
        pagina_selecionada = st.sidebar.selectbox("Selecione a Página", opcoes)
        
        if pagina_selecionada == "Dados":
            pagina_dados()
        elif pagina_selecionada == "Políticas Lançamentos":
            pagina_lancamentos()
        elif pagina_selecionada == "Políticas Pós":
            pagina_policas_pos()
        elif pagina_selecionada == "Avulsos":
            pagina_avulsos()
        elif pagina_selecionada == "Lançamentos":
            pagina_lancamentos_politicas()
        elif pagina_selecionada == "Pós":
            pagina_policas_pos()
    else:
        pagina_login()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()

#dotlemon\Scripts\activate

