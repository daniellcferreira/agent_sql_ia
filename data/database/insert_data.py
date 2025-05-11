from faker import Faker
import random
import mysql.connector

# função para inserir dados fakes
def insert_fake_data(cursor, n):
  """
  Insere dados fictícios nas tabelas 'clientes', 'enderecos', 'movimentacoes' e 'pagamentos'.

  Parâmetros:
    cursor: Objeto cursor do MySQL, utilizado para executar comandos SQL.
    n: Quantidade de registros a serem inseridos.
  """
  fake = Faker()  # Cria uma instância do Faker fora do loop para evitar repetição

  try:
    for _ in range(n):
      # Gera dados fictícios
      nome = fake.name()
      cpf = random.randint(11111111111, 99999999999)
      email = fake.email()

      # Inserção na tabela 'clientes'
      cursor.execute("""
        INSERT INTO clientes (nome, cpf, email) VALUES (%s, %s, %s)
      """, (nome, cpf, email))
      cliente_id = cursor.lastrowid  # Recupera o ID do cliente recém-inserido

      # Inserção na tabela 'enderecos'
      cursor.execute("""
        INSERT INTO enderecos (cliente_id, rua, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s)
      """, (cliente_id, fake.street_address(), fake.city(), fake.state(), fake.zipcode()))

      # Inserção na tabela 'movimentacoes'
      cursor.execute("""
        INSERT INTO movimentacoes (cliente_id, tipo_movimentacao, valor, data_movimentacao)
        VALUES (%s, %s, %s, %s)
      """, (
        cliente_id,
        random.choice(['depósito', 'saque', 'transferência']),
        round(random.uniform(50.0, 5000.0), 2),
        fake.date_this_year()
      ))

      # Inserção na tabela 'pagamentos'
      cursor.execute("""
        INSERT INTO pagamentos (cliente_id, valor, data_pagamento)
        VALUES (%s, %s, %s)
      """, (
        cliente_id,
        round(random.uniform(20.0, 1000.0), 2),
        fake.date_this_year()
      ))

  except mysql.connector.Error as err:
    # Captura de erro caso algo dê errado na inserção dos dados
    print(f"Erro ao inserir dados fictícios: {err}")
    raise  # Relevanta o erro para ser tratado onde necessário

  print("Dados fictícios inseridos com sucesso!")