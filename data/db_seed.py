import os
from dotenv import load_dotenv
from data.database.connection import get_connection
from data.database.schema import create_schema
from data.database.insert_data import insert_fake_data
from data.export.export_csv import export_to_csv

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Obtém o nome do banco de dados e o número de registros
DATABASE = os.getenv("MYSQL_DB")
N = 1000

# Verifica se a variável de ambiente do banco de dados foi carregada corretamente
if not DATABASE:
  print("Erro: A variável de ambiente MYSQL_DB não foi definida.")
  exit(1)

try:
  # Estabelece a conexão com o banco de dados
  conn = get_connection()
  cursor = conn.cursor()

  # Criação do esquema (tabelas)
  print("Criando o esquema no banco de dados...")
  create_schema(cursor, DATABASE)
  
  # Inserção de dados fictícios
  print(f"Inserindo {N} registros fictícios...")
  insert_fake_data(cursor, N)
  conn.commit()

  # Exportação dos dados para CSV
  print("Exportando dados para arquivos CSV...")
  export_to_csv(cursor, "SELECT * FROM clientes", "data/datasets/clientes.csv", ["cliente_id", "nome", "cpf", "email"])
  export_to_csv(cursor, "SELECT * FROM enderecos", "data/datasets/enderecos.csv", ["endereco_id", "cliente_id", "rua", "cidade", "estado", "cep"])
  export_to_csv(cursor, "SELECT * FROM movimentacoes", "data/datasets/movimentacoes.csv", ["movimentacao_id", "cliente_id", "tipo_movimentacao", "valor", "data_movimentacao"])
  export_to_csv(cursor, "SELECT * FROM pagamentos", "data/datasets/pagamentos.csv", ["pagamento_id", "cliente_id", "valor", "data_pagamento"])

except Exception as e:
  # Caso ocorra qualquer erro, imprime a mensagem e finaliza a execução
  print(f"Erro durante a execução: {e}")
  conn.rollback()  # Reverte qualquer alteração feita no banco
finally:
  # Garante que o cursor e a conexão sejam fechados, mesmo em caso de erro
  if cursor:
    cursor.close()
  if conn:
    conn.close()

print("Dados gerados com sucesso!")
