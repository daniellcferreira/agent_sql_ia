import openai
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# função para chamr a API do OenAI e gerar a query SQL
def gerar_query_sql(question: str, columns: dict) -> str:
  openai.api_key = os.getenv("OPENAI_API_KEY")

  # criação do prompt para o OpenAI, incluindo as colunas do banco
  prompt = f"""
    Você é um assistente de SQL que opera para o banco de dados ficticio chamado Dio Bank.
    Você deve gerar queries baseadas na seguinte estrutura do banco de dados:
    {columns}

    Pergunta: {question}
    Resposta em SQL:
    """
  
  # usando a nova API do OpenAI para chat
  response = openai.ChatCompletion.create(
    model= "gpt-4.1",
    messeges=[
      {"role": "system", "content": "Você é um assistente de SQL."},
      {"role": "user", "content": prompt}
    ],
    max_tokens=150,
    temperature=0
  )

  # obtendo a resposta gerada
  query = response['choices'][0]['message']['content'].strip()

  # remove qualquer marcação de codigo
  query = query.replace("```sql", "").replace("```", "").strip()

  return query

# função para obter as tabalas e colunas do banco de dados
def obter_estruturas_tabelas() -> dict:
  try:
    conn = mysql.connector.connect(
      host=os.getenv("MYSQL_HOST"),
      user=os.getenv("MYSQL_USER"),
      password=os.getenv("MYSQL_PASSWORD"),
      database=os.getenv("MYSQL_DB")
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tabelas = cursor.fetchall()

    colunas = {}
    for tabela in tabelas:
      cursor.execute(f"DESCRIBE {tabela[0]};")
      colunas_tabela = cursor.fetchall()
      colunas[tabela[0]] = [coluna[0] for coluna in colunas_tabela]

    cursor.close()
    conn.close()
    return colunas
  except Exception as e:
    return f"Erro ao obter estrutura das tabelas: {e}"
  
# função que executa a query SQL
def executar_query_func(query: str) -> str:
  try:
    conn = mysql.connector.connect(
      host=os.getenv("MYSQL_HOST", "localhost"),
      user=os.getenv("MYSQL_USER", "root"),
      password=os.getenv("MYSQL_PASSWORD", "admin123"),
      database=os.getenv("MYSQL_DB", "dioBank")
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results
  except:
    print('erro')

# exemplo de interação com o agente
question = input("Realize a sua pergunta ao nosso agente:")

# gera a query com base nas colunas
query_gerada = gerar_query_sql(question, obter_estruturas_tabelas())

print(f"\nQUERY GERADA: `{query_gerada}`")
print(f"RESULTADO")

# executa a query no banco de dados
print(executar_query_func(query_gerada))
