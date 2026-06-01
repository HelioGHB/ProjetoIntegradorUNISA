import sqlite3

def conectar_banco():
    return sqlite3.connect("estoque.db")

def inicializar_banco():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    
    # Tabela de produtos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_barras TEXT UNIQUE,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco_custo REAL,
            preco_venda REAL,
            quantidade INTEGER,
            quantidade_minima INTEGER,
            data_validade TEXT,
            usuario_cadastro TEXT
        )
    ''')
    
    # 3. Cria usuários padrão se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("admin", "1234"))
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", ("operador", "abc"))
    
    conexao.commit()
    conexao.close()

# Executa a criação das tabelas
inicializar_banco()