import mysql.connector

# Função para extrair a estrutura das tabelas do banco com base nas credenciais fornecidas
def obter_estruturas_tabelas(creds):
  try:
    conn = mysql.connector.connect(
      host=creds["mysql_host"],
      user=creds["mysql_user"],
      password=creds["mysql_password"],
      database=creds["mysql_db"]
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
  except:
    # Retorna um dicionário vazio se falhar (ex: conexão mal sucedida)
    return {}
