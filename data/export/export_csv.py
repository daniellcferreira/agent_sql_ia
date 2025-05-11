import csv
import mysql.connector

def export_to_csv(cursor, query, filename, headers):
  """
  Exporta os resultados de uma consulta SQL para um arquivo CSV.

  Parâmetros:
    cursor: Objeto cursor do MySQL, utilizado para executar comandos SQL.
    query: Consulta SQL a ser executada para obter os dados.
    filename: Nome do arquivo CSV para exportar os dados.
    headers: Cabeçalhos que serão usados na primeira linha do CSV.
  """
  try:
    # Executa a consulta no banco de dados
    cursor.execute(query)
    data = cursor.fetchall()  # Obtém todos os dados retornados pela consulta

    # Se houver dados, exporta para o arquivo CSV
    if data:
      with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)  # Escreve os cabeçalhos no arquivo CSV
        writer.writerows(data)    # Escreve os dados no arquivo CSV
      print(f"Exportado para {filename}")
    else:
      print(f"Sem dados para exportar na consulta: {query}")

  except mysql.connector.Error as err:
    # Captura erros durante a execução da consulta ou escrita do arquivo
    print(f"Erro ao exportar dados para CSV: {err}")
  except IOError as err:
    # Captura erros relacionados ao arquivo (por exemplo, problemas de permissão ou caminho inválido)
    print(f"Erro ao escrever no arquivo {filename}: {err}")
