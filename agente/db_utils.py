import mysql.connector
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para obter estrutura das tabelas no banco de dados
def obter_estruturas_tabelas() -> dict:
  """
  Obtém a estrutura das tabelas no banco de dados, ou seja, os nomes das colunas de cada tabela.

  Retorna:
    Um dicionário com os nomes das tabelas como chave e uma lista de colunas como valor.
  """
  try:
    # Conexão com o banco de dados MySQL
    conn = mysql.connector.connect( 
      host=os.getenv("MYSQL_HOST"),
      user=os.getenv("MYSQL_USER"),
      password=os.getenv("MYSQL_PASSWORD"),
      database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()

    # Obtém a lista de tabelas no banco de dados
    cursor.execute("SHOW TABLES;")
    tabelas = cursor.fetchall()

    # Dicionário para armazenar a estrutura das tabelas
    colunas = {}
    for tabela in tabelas:
      # Para cada tabela, obtém a descrição (colunas)
      cursor.execute(f"DESCRIBE {tabela[0]};")
      colunas_tabela = cursor.fetchall()
      colunas[tabela[0]] = [coluna[0] for coluna in colunas_tabela]

    cursor.close()
    conn.close()
    return colunas
  except Exception as e:
    raise Exception(f"Erro ao obter estrutura das tabelas: {e}")

# Função para executar uma query SQL no banco de dados
def executar_query_func(query: str):
  """
  Executa uma query SQL no banco de dados e retorna os resultados.

  Parâmetros:
    query: A query SQL a ser executada.

  Retorna:
    Os resultados da query executada.
  """
  try:
    # Conexão com o banco de dados MySQL
    conn = mysql.connector.connect(
      host=os.getenv("MYSQL_HOST", "localhost"),
      user=os.getenv("MYSQL_USER", "root"),
      password=os.getenv("MYSQL_PASSWORD", "admin123"),
      database=os.getenv("MYSQL_DB", "dioBank")
    )
    cursor = conn.cursor()

    # Executa a query passada como parâmetro
    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    return results
  except Exception as e:
    raise Exception(f"Erro na execução da query: {e}")
