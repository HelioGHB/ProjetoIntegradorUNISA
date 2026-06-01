# 📦 Sistema de Gestão de Estoque - Mercado Girassol

## 🎓 Informações Acadêmicas
* **Instituição:** Universidade Santo Amaro (UNISA)
* **Curso:** Graduação Tecnológica em Análise e Desenvolvimento de Sistemas
* **Disciplina:** Projeto Integrador - Desenvolvimento de Sistema
* **Estudante:** Greyke Hélio Barbosa Guilherme
* **Ano:** 2026

Para executar o código digite no terminal:
streamlit run app.py
---

## 📝 Descrição do Projeto
Este projeto apresenta uma solução digital automatizada para o gerenciamento de estoque voltada para pequenos varejos, tomando como estudo de caso o **Mercado Girassol** (um mercado de bairro). 

O objetivo central foi projetar e implementar um software que substitua o controle físico analógico (pranchetas, papel e anotações em cadernos) por uma plataforma digital segura, mitigando perdas financeiras decorrentes de erros humanos ou produtos vencidos, e fornecendo informações precisas em tempo real para a tomada de decisões estratégicas.

---

## 🚀 Funcionalidades Principais

* **🔒 Módulo de Autenticação de Usuários:** Tela de login centralizada e segura utilizando `st.session_state` para persistência de sessão e controle de acesso individualizado.
* **📝 Módulo de Cadastro de Mercadorias (Entradas):** Cadastro estruturado de produtos coletando atributos essenciais como Código de Barras (Chave Única), Nome, Categoria, Preço de Custo, Preço de Venda, Quantidade Inicial, Estoque Mínimo e Data de Validade.
* **👤 Rastreabilidade e Auditoria:** Vinculação automática de cada produto cadastrado ao usuário que realizou a operação no sistema.
* **📋 Dashboard de Estoque Atual:** Exibição dinâmica dos dados em tabela filtrável, com tratamento visual para registros nulos e validação de consistência.
* **📊 Indicadores Financeiros (Métricas):** Monitoramento em tempo real do total de itens distintos e do valor patrimonial total investido em estoque baseado nos preços de venda.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** [Python](https://www.python.org/)
* **Interface Gráfica (Frontend/Backend):** [Streamlit](https://streamlit.io/)
* **Análise de Dados:** [Pandas](https://pandas.pydata.org/)
* **Banco de Dados Relacional:** [SQLite](https://www.sqlite.org/) (Arquivo local `estoque.db`)

---

## 📂 Estrutura do Repositório

```text
├── database.py       # Script de conexão, criação e inicialização das tabelas do banco de dados
├── app.py            # Código-fonte principal com a interface Streamlit e regras de negócio
├── .gitignore        # Arquivo de configuração para ignorar ambiente virtual (venv) e banco local
├── requirements.txt  # Dependências e bibliotecas do projeto para instalação
└── README.md         # Documentação do projeto

Usuário, Senha, Nível de Acesso
admin,   1234,  Administrador / Gerente
operador, abc, Operador de Caixa / Estoquista

O Autor: Desenvolvido por Greyke Helio - Sinta-se à vontade para se conectar ou dar uma olhada nos meus outros projetos de programação! Linkedin: https://www.linkedin.com/in/greyke-h%C3%A9lio-20327a370/