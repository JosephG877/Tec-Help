import psycopg2
from psycopg2 import sql
from tkinter import messagebox, Tk

def create_database():
    try:
        # Conectar ao PostgreSQL para criar o banco de dados
        conn = psycopg2.connect(
            dbname='postgres',
            user='seu_usuario',
            password='sua_senha',
            host='localhost'
        )
        conn.autocommit = True  # Permite criar o banco de dados
        cursor = conn.cursor()

        # Nome do banco de dados para o sistema TEC HELP
        db_name = 'tec_help_db'

        # Verifica se o banco de dados já existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        exists = cursor.fetchone()

        if not exists:
            # Criar o banco de dados
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
            print(f"Banco de dados '{db_name}' criado com sucesso.")
        else:
            print(f"O banco de dados '{db_name}' já existe.")

        # Fechar a conexão com o banco de dados padrão
        cursor.close()
        conn.close()

        # Conectar ao novo banco de dados
        conn = psycopg2.connect(
            dbname=db_name,
            user='seu_usuario',
            password='sua_senha',
            host='localhost'
        )
        cursor = conn.cursor()

        # Criação das tabelas necessárias para o sistema TEC HELP
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            senha VARCHAR(255) NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chamados (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER REFERENCES usuarios(id),
            categoria_id INTEGER REFERENCES categorias_chamados(id),
            assunto_id INTEGER REFERENCES assuntos_chamados(id),
            descricao TEXT NOT NULL,
            status VARCHAR(50) DEFAULT 'Aberto',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorias_chamados (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assuntos_chamados (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS configuracoes (
            id SERIAL PRIMARY KEY,
            chave VARCHAR(100) NOT NULL UNIQUE,
            valor TEXT NOT NULL
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS localidades (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs_atividades (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER REFERENCES usuarios(id),
            descricao TEXT NOT NULL,
            data_atividade TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS mensagens_chamados (
            id SERIAL PRIMARY KEY,
            chamado_id INTEGER REFERENCES chamados(id),
            usuario_id INTEGER REFERENCES usuarios(id),
            mensagem TEXT NOT NULL,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')

        # Confirmar as mudanças
        conn.commit()

        print("Tabelas criadas com sucesso.")
        messagebox.showinfo("Sucesso", "Banco de dados e tabelas criados com sucesso!")

        # Fechar a conexão
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao criar o banco de dados: {e}")
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

def iniciar_instalacao():
    root = Tk()
    root.withdraw()  # Oculta a janela principal
    resposta = messagebox.askyesno("Instalador", "Deseja criar o banco de dados e suas tabelas?")
    
    if resposta:
        create_database()
    else:
        messagebox.showinfo("Instalador", "Instalação cancelada.")
    
    root.destroy()

if __name__ == "__main__":
    iniciar_instalacao()
