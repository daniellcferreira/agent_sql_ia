import csv
import random
import mysql.connector
from faker import Faker
from datetime import datetime
import os
from dotenv import load_dotenv

# carrega credenciais do MYSQL e declara variaveis
load_dotenv()
database = os.getenv("MYSQL_DB")
n = 1000

# conecta ao MYSQL
conn = mysql.connector.connect(
  host=os.getenv("MYSQL_HOST"),
  user=os.getenv("MYSQL_USER"),
  password=os.getenv("MYSQL_PASSWORD"),
  port=os.getenv("MYSQL_PORT")
)

cursor = conn.cursor()

# cria o banco de dados se não existir
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
conn.commit()

# conecta ao banco de dados correto
conn.database = database

#cria as tabelas no banco de dados
cursor.execute("""
  CREATE TABLE IF NOT EXISTS clientes (
    cliente_id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    cpf VARCHAR(11),
    email VARCHAR(100)
  )
""")

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

cursor.execute("""
  CREATE TABLE IF NOT EXISTS pagamentos (
    pagamento_id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    valor DECIMAL(10, 2),
    data_pagamento DATE,
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
  )
""")

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

# inicializa o FAKER para gerar dados fictícios
fake = Faker()

# função para exportar os dados para CSV
def export_to_csv(query, filename, headers):
  cursor.execute(query)
  data = cursor.fetchall()

  if data:
    with open(filename, "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerow(headers)
      writer.writerows(data)
    print(f"Exportando para {filename}")
  else:
    print(f"Sem dados para exportar na consulta: {query}")

# gera dados e insere na banco de dados
for linha in range(n):
  nome = fake.name()
  cpf = random.randint(11111111111,99999999999)
  email = fake.email()

  cursor.execute("""
        INSERT INTO clientes (nome, cpf, email)
        VALUES (%s, %s, %s)
    """, (nome, cpf, email))
  cliente_id = cursor.lastrowid

  # gera o endereço
  rua = fake.street_address()
  cidade = fake.city()
  estado = fake.state()
  cep = fake.zipcode()

  cursor.execute("""
        INSERT INTO enderecos (cliente_id, rua, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s)
    """, (cliente_id, rua, cidade, estado, cep))

  # gera movimentação bancária
  tipo_movimentacao = random.choice(['depósito', 'saque', 'transferência'])
  valor = round(random.uniform(50.0, 5000.0), 2)
  data_movimentacao = fake.date_this_year()

  cursor.execute("""
        INSERT INTO movimentacoes (cliente_id, tipo_movimentacao, valor, data_movimentacao)
        VALUES (%s, %s, %s, %s)
    """, (cliente_id, tipo_movimentacao, valor, data_movimentacao))
  
  # gera pagamento
  valor_pagamento = round(random.uniform(20.0, 1000.0), 2)
  data_pagamento = fake.date_this_year()

  cursor.execute("""
        INSERT INTO pagamentos (cliente_id, valor, data_pagamento)
        VALUES (%s, %s, %s)
    """, (cliente_id, valor_pagamento, data_pagamento))
  
# commit as mudanças no banco
conn.commit()

# exporta os dados das tabelas para CSV
export_to_csv("SELECT * FROM clientes", 'data/datasets/clientes.csv', ['cliente_id', 'nome', 'cpf', 'email'])
export_to_csv("SELECT * FROM enderecos", 'data/datasets/enderecos.csv', ['endereco_id', 'cliente_id', 'rua', 'cidade', 'estado', 'cep'])
export_to_csv("SELECT * FROM movimentacoes", 'data/datasets/movimentacoes.csv', ['movimentacao_id', 'cliente_id', 'tipo_movimentacao', 'valor', 'data_movimentacao'])
export_to_csv("SELECT * FROM pagamentos", 'data/datasets/pagamentos.csv', ['pagamento_id', 'cliente_id', 'valor', 'data_pagamento'])

# fecha a conexão com o banco de dados
cursor.close()
conn.close()