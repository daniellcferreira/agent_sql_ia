import mysql.connector

def create_schema(cursor, database):
  """
  Cria o banco de dados e as tabelas necessárias se não existirem.
  
  Parâmetros:
    cursor: Objeto cursor do MySQL, utilizado para executar comandos SQL.
    database: Nome do banco de dados a ser criado ou utilizado.
  """
  try:
    # Criação do banco de dados se não existir e seleção do banco
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    cursor.execute(f"USE {database}")

    # Criação da tabela 'clientes'
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS clientes (
        cliente_id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(100),
        cpf VARCHAR(11),
        email VARCHAR(100)
      )
    """)

    # Criação da tabela 'enderecos'
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS enderecos (
        endereco_id INT AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT,
        rua VARCHAR(255),
        cidade VARCHAR(100),
        estado VARCHAR(50),
        cep VARCHAR(8),
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
      )
    """)

    # Criação da tabela 'pagamentos'
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS pagamentos (
        pagamento_id INT AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT,
        valor DECIMAL(10, 2),
        data_pagamento DATE,
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
      )
    """)

    # Criação da tabela 'movimentacoes'
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS movimentacoes (
        movimentacao_id INT AUTO_INCREMENT PRIMARY KEY,
        cliente_id INT,
        tipo_movimentacao VARCHAR(50),
        valor DECIMAL(10, 2),
        data_movimentacao DATE,
        FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
      )
    """)
  
  except mysql.connector.Error as err:
    # Captura de erro caso algo dê errado na criação das tabelas
    print(f"Erro ao criar o esquema no banco de dados: {err}")
    raise  # Relevanta o erro para ser tratado onde necessário

  print("Esquema criado com sucesso!")