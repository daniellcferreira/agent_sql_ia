import os
import mysql.connector
from dotenv import load_dotenv

# Carrega variáveis de ambiente a partir de um arquivo .env
load_dotenv()

def get_connection():
  """
  Estabelece e retorna uma conexão com o banco de dados MySQL utilizando variáveis de ambiente.
  
  Retorna:
    mysql.connector.connect: Conexão com o banco de dados MySQL.
    
  Levanta:
    mysql.connector.Error: Caso ocorra um erro na conexão com o banco de dados.
  """
  try:
    # Tenta criar uma conexão com os parâmetros definidos nas variáveis de ambiente
    connection = mysql.connector.connect(
      host=os.getenv("MYSQL_HOST"),
      user=os.getenv("MYSQL_USER"),
      password=os.getenv("MYSQL_PASSWORD"),
      port=os.getenv("MYSQL_PORT"),
    )
    return connection  # Retorna a conexão estabelecida
  except mysql.connector.Error as err:
    # Se ocorrer um erro, imprime a mensagem e levanta o erro para tratamento posterior
    print(f"Erro ao conectar ao MySQL: {err}")
    raise  # Relevanta o erro para ser tratado onde for necessário
