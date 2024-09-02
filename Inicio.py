import streamlit as st
from pymongo import MongoClient
from urllib.parse import quote_plus
from bson.objectid import ObjectId

# Codificar a senha para incluir na URI
username = "leonardoaugusto199813"
password = quote_plus("August@123")


# Configuração do cliente MongoDB
#client = MongoClient('mongodb://localhost:27017/' , serverSelectionTimeoutMS=30000, socketTimeoutMS=30000 )
client = MongoClient(f'mongodb+srv://{username}:{password}@precificacao.axzys.mongodb.net/?retryWrites=true&w=majority&appName=Precificacao')
db = client.precificacao
colecao_login = db['login']
colecao_dados = db['answers_dados']
colecao_lancamentos = db['answers_lancamento']
colecao_pos = db['answers_pos']

def verificar_credenciais(login, senha):
    usuario = colecao_login.find_one({"login": login})
    if usuario:
        senha_armazenada = usuario.get("senha")
        tipo_usuario = usuario.get("tipo")
        cliente_id = usuario.get("cliente_id")  # Obter o ID do usuário
        return senha_armazenada == senha, tipo_usuario, cliente_id
    return False, None, None

# Página Login
def pagina_login():
    st.title("Página de Login")

    # Campos para o login
    login = st.text_input("Login", key="login_input_unico")
    senha = st.text_input("Senha", type='password', key="password_input_unico")

    if st.button("Entrar", key="entrar_button"):
        login_valido, tipo_usuario, cliente_id = verificar_credenciais(login, senha)
        if login_valido:
            st.session_state['login'] = True
            st.session_state['tipo_usuario'] = tipo_usuario  # Armazenar o tipo de usuário na sessão
            st.session_state['cliente_id'] = cliente_id  # Armazenar o ID do usuário na sessão
            st.session_state['dados_existentes'] = colecao_dados.find_one({"cliente_id": cliente_id}) or {}
            st.success("Login bem-sucedido!")
            st.rerun()  # Recarregar para refletir o estado de login
        else:
            st.error("Login ou senha incorretos.")

def pagina_dados():
    st.title('Dados')  # Título da página
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')  # Informativo

    # Inicializa os valores na sessão com dados existentes
    dados_existentes = st.session_state.get('dados_existentes', {})

    folha_pagamento = dados_existentes.get('folha_pagamento', 0.0)
    despesas_operacionais = dados_existentes.get('despesas_operacionais', 0.0)
    despesas_administrativas = dados_existentes.get('despesas_administrativas', 0.0)
    impostos_pagos = dados_existentes.get('impostos_pagos', 0.0)
    faturamento = dados_existentes.get('faturamento', 0.0)
    clientes_medios = dados_existentes.get('clientes_medios', 0)

    # Campos de entrada para os dados financeiros
    folha_pagamento = st.number_input("Gastos com Folha de Pagamento (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=folha_pagamento, key="folha_pagamento_input")
    despesas_operacionais = st.number_input("Despesas Operacionais (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=despesas_operacionais, key="despesas_operacionais_input")
    despesas_administrativas = st.number_input("Despesas Administrativas (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=despesas_administrativas, key="despesas_administrativas_input")
    impostos_pagos = st.number_input("Impostos Pagos (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=impostos_pagos, key="impostos_pagos_input")
    faturamento = st.number_input("Faturamento (Anual): R$", min_value=0.0, step=0.01, format="%.2f", value=faturamento, key="faturamento_input")
    clientes_medios = st.number_input("Quantidade média de Clientes (Mês):", min_value=0, step=1, format="%d", value=clientes_medios, key="clientes_medios_input")
    




    # Botão de enviar
    if st.button("Enviar", key="dados_enviar_button"):
        # Recuperar valores do session_state
        dados_novos = {
            "cliente_id": st.session_state['cliente_id'],
            "faturamento": faturamento,
            "clientes_medios": clientes_medios,
            "folha_pagamento": folha_pagamento,
            "despesas_operacionais": despesas_operacionais,
            "despesas_administrativas": despesas_administrativas,
            "impostos_pagos": impostos_pagos,
            "aliquota_imposto": (impostos_pagos / faturamento) * 100 if faturamento > 0 else 0,
            "custo_mensal_coberto": round((folha_pagamento + despesas_operacionais + despesas_administrativas) / 12, 2),
            "contribuicao_cliente": round((folha_pagamento + despesas_operacionais + despesas_administrativas)/12 / (clientes_medios if clientes_medios > 0 else 1), 2),
            "despesa_receita": round(((folha_pagamento + despesas_operacionais + despesas_administrativas)/12 / (faturamento / 12) if faturamento > 0 else 1) * 100, 2)
        }
        # Atualizar ou inserir os dados na coleção
        colecao_dados.update_one({"cliente_id": st.session_state['cliente_id']}, {'$set': dados_novos}, upsert=True)

        # Exibição das variáveis calculadas
        st.success("Valores enviados e gravados com sucesso!")
        st.write("### Valores Calculados")
        st.write(f"Alíquota de Imposto: {dados_novos['aliquota_imposto']:.0f}%")
        st.write(f"Custo Mensal Coberto: R$ {dados_novos['custo_mensal_coberto']:.2f}")
        st.write(f"Contribuição por Cliente: R$ {dados_novos['contribuicao_cliente']:.2f}")
        st.write(f"Despesa/Receita: {dados_novos['despesa_receita']:.0f}%")

# Função para exibir a página de Lançamentos
def pagina_lancamentos():
    st.title('POLÍTICAS LANÇAMENTOS')
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')

    # Recupera o ID do usuário da sessão
    cliente_id = st.session_state.get('cliente_id')
    if not cliente_id:
        st.error("Usuário não autenticado.")
        return

    # Inicializa valores na sessão se não existirem
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

    # Carrega os dados do MongoDB se disponíveis
    user_data = colecao_lancamentos.find_one({'cliente_id': cliente_id})
    if user_data:
        st.session_state['cliente_p'] = user_data.get('cliente_p', 0.0)
        st.session_state['cliente_m'] = user_data.get('cliente_m', 0.0)
        st.session_state['comissao_p'] = user_data.get('comissao_p', 0.0)
        st.session_state['comissao_m'] = user_data.get('comissao_m', 0.0)
        st.session_state['comissao_g'] = user_data.get('comissao_g', 0.0)

    # Cria inputs para os dados
    st.session_state['cliente_p'] = st.number_input("Cliente P (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_p']), key="cliente_p_input")
    st.session_state['cliente_m'] = st.number_input("Cliente M (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_m']), key="cliente_m_input")
    st.session_state['comissao_p'] = st.number_input("Cliente P (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_p']), key="comissao_p_input")
    st.session_state['comissao_m'] = st.number_input("Cliente M (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_m']), key="comissao_m_input")
    st.session_state['comissao_g'] = st.number_input("Cliente G (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_g']), key="comissao_g_input")

    if st.button("Enviar", key="lancamentos_enviar_button"):
        cliente_p = st.session_state['cliente_p']
        cliente_m = st.session_state['cliente_m']
        comissao_p = st.session_state['comissao_p']
        comissao_m = st.session_state['comissao_m']
        comissao_g = st.session_state['comissao_g']

        # Define o dicionário de dados a ser atualizado ou inserido
        dados_lancamentos = {
            "cliente_id": cliente_id,  # Use o cliente_id diretamente se não for um ObjectId
            "cliente_p": cliente_p,
            "cliente_m": cliente_m,
            "comissao_p": comissao_p,
            "comissao_m": comissao_m,
            "comissao_g": comissao_g
        }

        # Atualiza ou insere os dados na coleção
        colecao_lancamentos.update_one(
            {"cliente_id": cliente_id},  # Use o cliente_id diretamente na consulta
            {'$set': dados_lancamentos},
            upsert=True
        )

        st.success("Dados enviados com sucesso!")


# Função para exibir a página de Lançamentos pos
def pagina_policas_pos():
    st.title('POLÍTICAS PÓS')
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')

    # Recupera o ID do usuário da sessão
    cliente_id = st.session_state.get('cliente_id')
    if not cliente_id:
        st.error("Usuário não autenticado.")
        return

    # Inicializa os valores na sessão se não existirem
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

    # Carrega os dados do MongoDB se disponíveis
    user_data = colecao_pos.find_one({'cliente_id': cliente_id})
    if user_data:
        st.session_state['cliente_p2'] = user_data.get('cliente_p2', 0.0)
        st.session_state['cliente_m2'] = user_data.get('cliente_m2', 0.0)
        st.session_state['comissao_p2'] = user_data.get('comissao_p2', 0.0)
        st.session_state['comissao_m2'] = user_data.get('comissao_m2', 0.0)
        st.session_state['comissao_g2'] = user_data.get('comissao_g2', 0.0)

    # Cria inputs para os dados
    st.session_state['cliente_p2'] = st.number_input("Cliente P (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_p2']), key="cliente_p2_input")
    st.session_state['cliente_m2'] = st.number_input("Cliente M (Faturamento Máximo)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['cliente_m2']), key="cliente_m2_input")
    st.session_state['comissao_p2'] = st.number_input("Cliente P (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_p2']), key="comissao_p2_input")
    st.session_state['comissao_m2'] = st.number_input("Cliente M (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_m2']), key="comissao_m2_input")
    st.session_state['comissao_g2'] = st.number_input("Cliente G (% Comissão)", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['comissao_g2']), key="comissao_g2_input")

    if st.button("Enviar", key="pos_enviar_button"):
        cliente_p2 = st.session_state['cliente_p2']
        cliente_m2 = st.session_state['cliente_m2']
        comissao_p2 = st.session_state['comissao_p2']
        comissao_m2 = st.session_state['comissao_m2']
        comissao_g2 = st.session_state['comissao_g2']

        # Define o dicionário de dados a ser atualizado ou inserido
        dados_pos = {
            "cliente_id": cliente_id,  # Use o cliente_id diretamente
            "cliente_p2": cliente_p2,
            "cliente_m2": cliente_m2,
            "comissao_p2": comissao_p2,
            "comissao_m2": comissao_m2,
            "comissao_g2": comissao_g2
        }

        # Atualiza ou insere os dados na coleção
        colecao_pos.update_one(
            {'cliente_id': cliente_id},  # Use o cliente_id diretamente na consulta
            {'$set': dados_pos},
            upsert=True
        )

        st.success("Dados enviados com sucesso!")


def pagina_avulsos():
    st.title('AVULSOS')
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')

    # Recupera o ID do usuário da sessão
    cliente_id = st.session_state.get('cliente_id')
    if not cliente_id:
        st.error("Usuário não autenticado.")
        return

    # Inicializa os valores na sessão
    default_value = 0.0
    if 'folha_pagamento2' not in st.session_state:
        st.session_state['folha_pagamento2'] = default_value
    if 'folha_pagamento3' not in st.session_state:
        st.session_state['folha_pagamento3'] = default_value
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

    # Busca a alíquota de imposto da coleção 'answer_dados' com base no cliente_id
    aliquota_imposto = default_value
    dados_fiscais = colecao_dados.find_one({'cliente_id': cliente_id})
    if dados_fiscais:
        aliquota_imposto = dados_fiscais.get('aliquota_imposto', default_value)
    
    # Salva a alíquota na sessão
    st.session_state['aliquota_imposto'] = aliquota_imposto

    # Campos de entrada para os dados financeiros
    st.session_state['folha_pagamento2'] = st.number_input("% Reinvestimento", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento2'], key="folha_pagamento2_input")
    st.session_state['folha_pagamento3'] = st.number_input("% Margem", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento3'], key="folha_pagamento3_input")
    st.session_state['folha_pagamento4'] = st.number_input("Custo hora Copy", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento4'], key="folha_pagamento4_input")
    st.session_state['folha_pagamento5'] = st.number_input("Horas Gastas Copy", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento5'], key="folha_pagamento5_input")
    st.session_state['folha_pagamento6'] = st.number_input("Custo Hora Design", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento6'], key="folha_pagamento6_input")
    st.session_state['folha_pagamento7'] = st.number_input("Horas Gastas Design", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento7'], key="folha_pagamento7_input")
    st.session_state['folha_pagamento8'] = st.number_input("Custo Hora Trafego", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento8'], key="folha_pagamento8_input")
    st.session_state['folha_pagamento9'] = st.number_input("Horas Gastas Trafego", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento9'], key="folha_pagamento9_input")
    st.session_state['folha_pagamento10'] = st.number_input("Custo Hora Automação", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento10'], key="folha_pagamento10_input")
    st.session_state['folha_pagamento11'] = st.number_input("Horas Gastas Automação", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento11'], key="folha_pagamento11_input")
    st.session_state['folha_pagamento12'] = st.number_input("Custo Hora Inbound", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento12'], key="folha_pagamento12_input")
    st.session_state['folha_pagamento13'] = st.number_input("Horas Gastas Inbound", min_value=0.0, step=0.01, format="%.2f", value=st.session_state['folha_pagamento13'], key="folha_pagamento13_input")

    # Botão de enviar
    if st.button("Enviar", key="avulsos_enviar_button"):
        folha_pagamento2 = st.session_state['folha_pagamento2']
        folha_pagamento3 = st.session_state['folha_pagamento3']
        folha_pagamento4 = st.session_state['folha_pagamento4']
        folha_pagamento5 = st.session_state['folha_pagamento5']
        folha_pagamento6 = st.session_state['folha_pagamento6']
        folha_pagamento7 = st.session_state['folha_pagamento7']
        folha_pagamento8 = st.session_state['folha_pagamento8']
        folha_pagamento9 = st.session_state['folha_pagamento9']
        folha_pagamento10 = st.session_state['folha_pagamento10']
        folha_pagamento11 = st.session_state['folha_pagamento11']
        folha_pagamento12 = st.session_state['folha_pagamento12']
        folha_pagamento13 = st.session_state['folha_pagamento13']
        aliquota_imposto = st.session_state['aliquota_imposto']
        
        total_horass = folha_pagamento13 + folha_pagamento11 + folha_pagamento7 + folha_pagamento9 + folha_pagamento5
        custo_total = (folha_pagamento4 * folha_pagamento5) + (folha_pagamento10 * folha_pagamento11) + (folha_pagamento6 * folha_pagamento7) + (folha_pagamento12 * folha_pagamento13) + (folha_pagamento8 * folha_pagamento9)
        fator_preco = 1 / (1 - (round((folha_pagamento2 / 100),2) + round((folha_pagamento3 / 100),2) + round((aliquota_imposto / 100),2)))
        p_final = custo_total * fator_preco

        st.success("Enviado com sucesso!")
        st.write("### Valores Calculados")
        st.write(f"Total de Horas: {total_horass:.0f}")
        st.write(f"Custo Total: {custo_total:.2f}")
        st.write(f"Fator preço: {fator_preco:.2f}")
        st.write(f"Preço Final: {p_final:.0f}")


# Função para exibir a página de Lançamentos Políticas
def pagina_lancamentos_politicas():
    st.title('LANÇAMENTOS')
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')

    # Recupera o ID do usuário da sessão
    cliente_id = st.session_state.get('cliente_id')
    if not cliente_id:
        st.error("Usuário não autenticado.")
        return

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
    st.session_state['projeto_meses'] = st.number_input("Total de Meses do Projeto", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['projeto_meses']), key="projeto_meses_input")
    st.session_state['fat_lancamento'] = st.number_input("Faturamento", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['fat_lancamento']), key="fat_lancamento_input")
    st.session_state['traf'] = st.number_input("Trafego %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['traf']), key="traf_input")
    st.session_state['plat'] = st.number_input("Plataforma %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['plat']), key="plat_input")
    st.session_state['imp'] = st.number_input("Imposto %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['imp']), key="imp_input")

    # Busca o valor de contribuicao_cliente na coleção 'answers_dados' com base no cliente_id
    contribuicao_cliente = 0.0
    dados_fiscais = colecao_dados.find_one({'cliente_id': cliente_id})
    if dados_fiscais:
        contribuicao_cliente = dados_fiscais.get('contribuicao_cliente', 0.0)

    # Salva a contribuicao_cliente na sessão
    st.session_state['contribuicao_cliente'] = contribuicao_cliente

    if st.button("Enviar", key="lancamentos_politicas_enviar_button"):
        projeto_meses = st.session_state['projeto_meses']
        fat_lancamento = st.session_state['fat_lancamento']
        traf = st.session_state['traf']
        plat = st.session_state['plat']
        imp = st.session_state['imp']

        st.session_state['traf_valor'] = round(fat_lancamento * (traf / 100), 3)
        traf_valor = st.session_state['traf_valor']
        st.session_state['plat_valor'] = round(fat_lancamento * (plat / 100), 3)
        plat_valor = st.session_state['plat_valor']
        st.session_state['imp_valor'] = round(fat_lancamento * (imp / 100), 3)
        imp_valor = st.session_state['imp_valor']
        st.session_state['depesas'] = traf_valor + plat_valor + imp_valor
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
        st.write(f'Despesas R$: {despesas} ')

        percentuais_politicas = (traf / 100) + (plat / 100) + (imp / 100)

        if fat_lancamento <= cliente_p:
            faixa1 = (fat_lancamento - despesas) * (comissao_p / 100)
            faixa2 = 0
            faixa3 = 0
            st.write(f'Comissão Faixa 1 R$: {faixa1}')
        else:
            faixa1 = (cliente_p - (cliente_p * (percentuais_politicas))) * (comissao_p / 100)
            st.write(f'Comissão Faixa 1 R$: {faixa1}')

        depesas_clientep = cliente_p * percentuais_politicas
        depesas_clientem = cliente_m * percentuais_politicas

        if fat_lancamento <= cliente_p:
            faixa2 = 0
            faixa3 = 0
        elif fat_lancamento <= cliente_m:
            parte1 = fat_lancamento - cliente_p
            subtracao_despesas = despesas - depesas_clientep
            faixa2 = (parte1 - subtracao_despesas) * (comissao_m / 100)
            st.write(f'Comissão Faixa 2 : R${faixa2}')
        else:
            faixa3 = 0
            subtracao_faixas = cliente_m - cliente_p
            subtracao_despesas = depesas_clientem - depesas_clientep
            faixa2 = (subtracao_faixas - subtracao_despesas) * (comissao_m / 100)
            st.write(f'Comissão Faixa 2 : R${faixa2}')

        if fat_lancamento > cliente_m:
            parte1 = fat_lancamento - cliente_m
            subtracao_despesas = despesas - depesas_clientem
            faixa3 = (parte1 - subtracao_despesas) * (comissao_g / 100)
            st.write(f'Comissão Faixa 3 : R${faixa3}')
        else:
            faixa3 = 0

        umenosaliquota = 1 - (aliquota_imposto / 100)
        comissao_recebida = faixa1 + faixa2 + faixa3
        st.write(f'Recebido a título de comissão R$: {comissao_recebida}')

        tx_fix_mensal = round(contribuicao_cliente / umenosaliquota, 2)
        st.write(f'Taxa Fixa Mensal: {tx_fix_mensal}')
        total_recebido = tx_fix_mensal * projeto_meses + comissao_recebida
        st.write(f'Total Recebido no Projeto: R${round(total_recebido, 2)}')


# Função para exibir a página de Pós
def pagina_pos_politicas():
    st.title('Pós')
    st.info('🟡 Preencha os campos com as informações solicitadas 🟡')

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
    st.session_state['projeto_meses_pos'] = st.number_input("Total de Meses do Projeto", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['projeto_meses_pos']), key="projeto_meses_pos_input")
    st.session_state['fat_lancamento_pos'] = st.number_input("Faturamento", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['fat_lancamento_pos']), key="fat_lancamento_pos_input")
    st.session_state['traf_pos'] = st.number_input("Trafego %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['traf_pos']), key="traf_pos_input")
    st.session_state['plat_pos'] = st.number_input("Plataforma %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['plat_pos']), key="plat_pos_input")
    st.session_state['imp_pos'] = st.number_input("Imposto %", min_value=0.0, step=0.01, format="%.2f", value=float(st.session_state['imp_pos']), key="imp_pos_input")

    if st.button("Enviar", key="pos_politicas_enviar_button"):
        projeto_meses_pos = st.session_state['projeto_meses_pos']
        fat_lancamento_pos = st.session_state['fat_lancamento_pos']
        traf_pos = st.session_state['traf_pos']
        plat_pos = st.session_state['plat_pos']
        imp_pos = st.session_state['imp_pos']

        st.session_state['traf_pos_valor'] = round(fat_lancamento_pos * (traf_pos/100), 3)
        traf_pos_valor = st.session_state['traf_pos_valor']
        st.session_state['plat_pos_valor'] = round(fat_lancamento_pos * (plat_pos/100), 3)
        plat_pos_valor = st.session_state['plat_pos_valor']
        st.session_state['imp_pos_valor'] = round(fat_lancamento_pos * (imp_pos/100), 3)
        imp_pos_valor = st.session_state['imp_pos_valor']
        st.session_state['despesas_Pos'] = traf_pos_valor + plat_pos_valor + imp_pos_valor
        despesas_Pos = st.session_state['despesas_Pos']

        comissao_p2 = st.session_state['comissao_p2']
        cliente_p2 = st.session_state['cliente_p2']
        comissao_m2 = st.session_state['comissao_m2']
        cliente_m2 = st.session_state['cliente_m2']
        comissao_g2 = st.session_state['comissao_g2']
        contribuicao_cliente = st.session_state['contribuicao_cliente']
        aliquota_imposto = st.session_state['aliquota_imposto']

        st.success("Dados enviados com sucesso!")
        st.write(f'Tráfego R$: {traf_pos_valor} ')
        st.write(f'Plataforma R$: {plat_pos_valor} ')
        st.write(f'Imposto R$: {imp_pos_valor} ')
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
            faixa3 = 0
            subtracao_faixas = cliente_m2-cliente_p2
            subtracao_despesas = depesas_clientem-depesas_clientep
            faixa2 = (subtracao_faixas-subtracao_despesas)*(comissao_m2/100)
            st.write(f'Comissão Faixa 2 : R${faixa2}')

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
def main():
    if 'login' not in st.session_state:
        st.session_state['login'] = False
        st.session_state['tipo_usuario'] = None  # Inicializar tipo_usuario na sessão

    if st.session_state['login']:
        if st.session_state['tipo_usuario'] == 1:
            opcoes = ["Dados", "Políticas Lançamentos", "Políticas Pós", "Avulsos", "Lançamentos", "Pós"]
        else:
            opcoes = ["Avulsos", "Lançamentos", "Pós"]
        
        pagina_selecionada = st.sidebar.selectbox("Selecione a Página", opcoes, key="selectbox_pagina")
        
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
            pagina_pos_politicas()
    else:
        pagina_login()

if __name__ == "__main__":
    main()



#dotlemon\Scripts\activate

