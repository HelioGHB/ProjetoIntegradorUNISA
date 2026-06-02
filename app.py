import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
from database import conectar_banco

# Configuração inicial da página
st.set_page_config(page_title="Gestão de Estoque", page_icon="📦", layout="wide")
st.markdown("""
    <style>
        .stAppDeployButton {display:none;}
    </style>
""", unsafe_allow_html=True)

# Condições para o Login
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_atual" not in st.session_state:
    st.session_state.usuario_atual = None

# Funções autenticação
def verificar_login(usuario, senha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        return resultado is not None
    except sqlite3.OperationalError:
        # Caso a tabela de usuários ainda não exista ou esteja corrompida
        return False
    finally:
        conexao.close()

# Funções para o banco de dados
def cadastrar_produto(codigo_barras, nome, categoria, preco_custo, preco_venda, quantidade, qtd_minima, validade, usuario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        sql = '''INSERT INTO produtos 
                 (codigo_barras, nome, categoria, preco_custo, preco_venda, quantidade, quantidade_minima, data_validade, usuario_cadastro)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        valores = (codigo_barras, nome, categoria, preco_custo, preco_venda, quantidade, qtd_minima, validade, usuario)
        cursor.execute(sql, valores)
        conexao.commit()
        return True, "Produto cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "Erro: Este código de barras já está cadastrado!"
    except Exception as e:
        return False, f"Erro inesperado: {e}"
    finally:
        conexao.close()

def carregar_estoque():
    conexao = conectar_banco()
    try:
        df = pd.read_sql_query("SELECT * FROM produtos", conexao)
        return df
    except Exception:
        return pd.DataFrame(columns=['id', 'codigo_barras', 'nome', 'categoria', 'preco_custo', 'preco_venda', 'quantidade', 'quantidade_minima', 'data_validade', 'usuario_cadastro'])
    finally:
        conexao.close()

# Login

if not st.session_state.autenticado:
    # Centraliza o formulário
    col_esq, col_centro, col_dir = st.columns([1, 1.8, 1])
    
    with col_centro:
        st.write("")
        st.write("")
        st.write("")
        
        with st.container(border=True):
            st.markdown("<h2 style='text-align: center; margin-bottom: 5px;'> Login</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; color: gray; margin-bottom: 25px;'>Mercado Girassol</p>", unsafe_allow_html=True)
            
            with st.form(key="form_login", clear_on_submit=False):
                usuario_input = st.text_input("Usuário", placeholder="Digite seu usuário")
                senha_input = st.text_input("Senha", type="password", placeholder="Digite sua senha")
                
                botao_login = st.form_submit_button("Entrar", use_container_width=True)
                
                if botao_login:
                    if verificar_login(usuario_input, senha_input):
                        st.session_state.autenticado = True
                        st.session_state.usuario_atual = usuario_input
                        st.rerun()
                    else:
                        st.error("Usuário ou senha incorretos.")


# Tela principal se autenticado

else:
    # Barra lateral de controle do usuário
    st.sidebar.title(f"👤 {st.session_state.usuario_atual}")
    st.sidebar.markdown("---")
    if st.sidebar.button("Sair / Logout", use_container_width=True):
        st.session_state.autenticado = False
        st.session_state.usuario_atual = None
        st.rerun()

    # Cabeçalho da página principal
    st.title("Mercado Girassol")
    st.markdown("Painel de controle para o Mercado de Bairro")

    # Adicionada a aba de Alertas
    aba_cadastro, aba_estoque, aba_alertas = st.tabs(["Cadastrar Produto", "Visualizar Estoque", "⚠️ Alertas e Validade"])

    # Cadastro de produtos
    with aba_cadastro:
        st.header("Novo Produto")
        
        with st.form(key="form_cadastro", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                codigo_barras = st.text_input("Código de Barras (Opcional)")
                nome = st.text_input("Nome do Produto*")
                categoria = st.selectbox("Categoria", ["Alimentos Básicos", "Limpeza", "Bebidas", "Hortifruti", "Outros"])
                validade = st.date_input("Data de Validade", format="DD/MM/YYYY")
                
            with col2:
                preco_custo = st.number_input("Preço de Custo (R$)", min_value=0.0, format="%.2f", value=None, placeholder="0,00")
                preco_venda = st.number_input("Preço de Venda (R$)", min_value=0.0, format="%.2f", value=None, placeholder="0,00")
                quantidade = st.number_input("Quantidade Inicial", min_value=0, step=1, value=None, placeholder="0")
                qtd_minima = st.number_input("Estoque Mínimo (Alerta)", min_value=1, value=5, step=1)
                
            submit_button = st.form_submit_button(label="Cadastrar Produto no Estoque")
            
            if submit_button:
                if not nome.strip():
                    st.warning("O campo 'Nome do Produto' é obrigatório!")
                else:
                    codigo_barras_final = codigo_barras.strip() if codigo_barras.strip() != "" else None
                    p_custo_final = preco_custo if preco_custo is not None else 0.0
                    p_venda_final = preco_venda if preco_venda is not None else 0.0
                    qtd_final = quantidade if quantidade is not None else 0
                    validade_formatada = validade.strftime('%d/%m/%Y')
                    
                    # Salva o produto passando quem está logado no momento
                    sucesso, mensagem = cadastrar_produto(
                        codigo_barras_final, nome, categoria, p_custo_final, p_venda_final, 
                        qtd_final, qtd_minima, validade_formatada, st.session_state.usuario_atual
                    )
                    if sucesso:
                        st.success(f"{mensagem}")
                    else:
                        st.error(f"{mensagem}")

    # Carregar a base de dados uma única vez para usar nas abas seguintes
    df_estoque = carregar_estoque()

    # Visualizar Estoque
    with aba_estoque:
        st.header("Estoque Atual")
        
        if df_estoque.empty or len(df_estoque.columns) < 10:
            st.info("Nenhum produto cadastrado no momento. Vá para a aba de cadastro para inserir o primeiro item.")
        else:
            try:
                # Criando uma cópia para não afetar as outras abas
                df_exibicao = df_estoque.copy()
                df_exibicao.columns = ['ID', 'Código', 'Nome', 'Categoria', 'Custo (R$)', 'Venda (R$)', 'Qtd', 'Qtd Mínima', 'Validade', 'Cadastrado Por']
                
                # Tratamento para registros vazios
                df_exibicao['Código'] = df_exibicao['Código'].fillna("Não Cadastrado")
                df_exibicao['Cadastrado Por'] = df_exibicao['Cadastrado Por'].fillna("Sistema")
                
                # Exibição da tabela limpa
                st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
                
                st.divider()
                st.subheader("Resumo do Negócio")
                col_res1, col_res2 = st.columns(2)
                col_res1.metric("Total de Itens Diferentes", len(df_exibicao))
                col_res2.metric("Valor Total em Estoque (Venda)", f"R$ {(df_exibicao['Venda (R$)'] * df_exibicao['Qtd']).sum():.2f}")
            except Exception as e:
                st.error(f"Erro ao organizar visualização dos dados: {e}")

    # Aba de Alertas (Nova Seção)
    with aba_alertas:
        st.header("Painel de Alertas")
        
        if df_estoque.empty:
            st.info("Nenhum produto cadastrado para gerar alertas.")
        else:
            # Padronizar nomes de colunas internos para facilitar a busca
            df_alertas = df_estoque.copy()
            df_alertas.columns = ['ID', 'Codigo', 'Nome', 'Categoria', 'Custo', 'Venda', 'Qtd', 'Qtd_Minima', 'Validade', 'Usuario']
            
            # Produtos com baixo estoque
            st.subheader("Estoque Baixo ou Crítico")
            
            # Condição: Quantidade atual é menor ou igual à quantidade mínima configurada
            df_baixo_estoque = df_alertas[df_alertas['Qtd'] <= df_alertas['Qtd_Minima']]
            
            if not df_baixo_estoque.empty:
                st.error(f"Atenção: Existem {len(df_baixo_estoque)} produto(s) com quantidade igual ou abaixo do mínimo!")
                # Seleciona apenas colunas relevantes para exibição amigável
                st.dataframe(
                    df_baixo_estoque[['Nome', 'Categoria', 'Qtd', 'Qtd_Minima']], 
                    use_container_width=True, 
                    hide_index=True
                )
            else:
                st.success("Todos os produtos estão com níveis de estoque saudáveis.")
                
            st.divider()
            
            # Produtos próximos de vencer
            st.subheader("📅 Alerta de Validade")
            
            # Configuração de quantos dias de antecedência você quer ser avisado (ex: 30 dias)
            DIAS_PARA_ALERTA = 30
            
            hoje = datetime.now().date()
            produtos_vencidos = []
            produtos_perto_vencer = []
            
            # Loop para ler as datas salvas como string do SQLite e converter para comparação
            for index, row in df_alertas.iterrows():
                try:
                    # Converte o padrão 'DD/MM/YYYY' de volta para formato de data real
                    data_val = datetime.strptime(row['Validade'], '%d/%m/%Y').date()
                    dias_restantes = (data_val - hoje).days
                    
                    dados_prod = {
                        "Nome": row['Nome'],
                        "Categoria": row['Categoria'],
                        "Validade": row['Validade'],
                        "Qtd": row['Qtd'],
                        "Dias Restantes": dias_restantes
                    }
                    
                    if dias_restantes < 0:
                        produtos_vencidos.append(dados_prod)
                    elif 0 <= dias_restantes <= DIAS_PARA_ALERTA:
                        produtos_perto_vencer.append(dados_prod)
                except Exception:
                    # Ignora linhas que por ventura tenham erros de digitação na data
                    pass

            # Exibe os já vencidos (Crítico)
            if produtos_vencidos:
                st.error(f"🔴 CRÍTICO: Existem {len(produtos_vencidos)} produto(s) JÁ VENCIDO(S) no estoque!")
                df_vencidos = pd.DataFrame(produtos_vencidos)
                st.dataframe(df_vencidos[['Nome', 'Categoria', 'Validade', 'Qtd']], use_container_width=True, hide_index=True)
            
            # Exibe os próximos de vencer
            if produtos_perto_vencer:
                st.warning(f"🟡 ATENÇÃO: Existem {len(produtos_perto_vencer)} produto(s) que vencem nos próximos {DIAS_PARA_ALERTA} dias!")
                df_perto = pd.DataFrame(produtos_perto_vencer)
                # Ordena pelos que vão vencer mais rápido primeiro
                df_perto = df_perto.sort_values(by="Dias Restantes")
                st.dataframe(df_perto[['Nome', 'Categoria', 'Validade', 'Dias Restantes', 'Qtd']], use_container_width=True, hide_index=True)
                
            if not produtos_vencidos and not produtos_perto_vencer:
                st.success(f"Nenhum produto vencido ou vencendo nos próximos {DIAS_PARA_ALERTA} dias.")