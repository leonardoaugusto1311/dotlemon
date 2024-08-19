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
        return senha_armazenada == senha
    return False

# Página Login
def pagina_login():
    st.title("Página de Login")

    # Campos para o login
    login = st.text_input("Login")
    senha = st.text_input("Senha", type='password')

    if st.button("Entrar"):
        if verificar_credenciais(login, senha):
            st.session_state['login'] = True
            st.success("Login bem-sucedido!")
            st.rerun()  # Recarregar para refletir o estado de login
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

# Função principal para gerenciar a navegação
def main():
    if 'login' not in st.session_state:
        st.session_state['login'] = False

    if st.session_state['login']:
        # Menu de navegação após login bem-sucedido
        pagina_selecionada = st.sidebar.selectbox("Selecione a Página", ["Dados", "Políticas Lançamentos","Políticas Pós"])
        
        if pagina_selecionada == "Dados":
            pagina_dados()
        elif pagina_selecionada == "Políticas Lançamentos":
            pagina_lancamentos()
        elif pagina_selecionada == "Políticas Pós":
            pagina_policas_pos
    else:
        pagina_login()

if __name__ == "__main__":
    main()
