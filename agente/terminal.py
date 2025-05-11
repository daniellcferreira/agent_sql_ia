from agente.agent import gerar_query_sql
from agente.db_utils import obter_estruturas_tabelas, executar_query_func

# Função principal
def main():
  """
  Função principal que realiza a interação com o usuário, gera a query SQL
  com base na pergunta do usuário e exibe os resultados da execução da query.
  """
  # Solicita a pergunta ao usuário
  question = input("Realize a sua pergunta ao nosso agente: ")
  
  try:
    # Obtém a estrutura das tabelas
    colunas = obter_estruturas_tabelas()

    # Gera a query SQL com base na pergunta e na estrutura das tabelas
    query_gerada = gerar_query_sql(question, colunas)

    # Exibe a query gerada
    print(f"\nQUERY GERADA:\n{query_gerada}")
    print(f"\nRESULTADO:")

    # Executa a query e exibe os resultados
    resultado = executar_query_func(query_gerada)
    for linha in resultado:
      print(linha)

  except Exception as e:
    # Em caso de erro, exibe a mensagem de erro
    print(f"Ocorreu um erro: {e}")

# Executa a função principal se o script for executado diretamente
if __name__ == "__main__":
  main()
