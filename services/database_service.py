import mysql.connector

# Executa uma consulta SQL e retorna colunas e resultados
def executar_query_sql(query, creds):
  try:
    with mysql.connector.connect(
      host=creds["mysql_host"],
      user=creds["mysql_user"],
      password=creds["mysql_password"],
      database=creds["mysql_db"]
    ) as conn:
      with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return columns, result
  except Exception as e:
    print(f"Erro na execução da query: {e}")
    return [], []

# Salva pergunta, query gerada e resultado em histórico de interações
def salvar_historico(pergunta, query, resultado, creds):
  try:
    with mysql.connector.connect(
      host=creds["mysql_host"],
      user=creds["mysql_user"],
      password=creds["mysql_password"],
      database=creds["mysql_db"]
    ) as conn:
      with conn.cursor() as cursor:
        cursor.execute("""
          CREATE TABLE IF NOT EXISTS historico_interacoes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            pergunta TEXT,
            query_gerada TEXT,
            resultado LONGTEXT,
            feedback VARCHAR(10),
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
          );
        """)
        cursor.execute("""
          INSERT INTO historico_interacoes (pergunta, query_gerada, resultado)
          VALUES (%s, %s, %s);
        """, (pergunta, query, str(resultado)))
        conn.commit()
  except Exception as e:
    print(f"Erro ao salvar histórico: {e}")

# Atualiza o feedback da última pergunta feita (mais recentemente salva)
def salvar_feedback(pergunta, feedback, creds):
  try:
    with mysql.connector.connect(
      host=creds["mysql_host"],
      user=creds["mysql_user"],
      password=creds["mysql_password"],
      database=creds["mysql_db"]
    ) as conn:
      with conn.cursor() as cursor:
        cursor.execute("""
          UPDATE historico_interacoes
          SET feedback = %s
          WHERE pergunta = %s
          ORDER BY data DESC
          LIMIT 1;
        """, (feedback, pergunta))
        conn.commit()
  except Exception as e:
    print(f"Erro ao salvar feedback: {e}")
