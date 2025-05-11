import openai
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Valida se a chave de API foi carregada corretamente
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
  raise ValueError("A chave de API do OpenAI não foi definida no arquivo .env.")

openai.api_key = openai_api_key

# Função para gerar a query SQL a partir de uma pergunta
def gerar_query_sql(question: str, columns: dict) -> str:
  """
  Gera uma consulta SQL com base na pergunta fornecida e na estrutura do banco de dados.

  Parâmetros:
    question: Pergunta em linguagem natural sobre o banco de dados.
    columns: Estrutura do banco de dados (geralmente um dicionário) que descreve as tabelas e colunas.

  Retorna:
    A consulta SQL gerada pela IA.
  """
  prompt = f"""
  Você é um assistente de SQL que opera para o banco de dados fictício chamado Dio Bank.
  Você deve gerar queries baseadas na seguinte estrutura do banco de dados:
  {columns}

  Pergunta: {question}
  Resposta em SQL:
  """
  
  try:
    # Chama a API do OpenAI para gerar a consulta SQL
    response = openai.ChatCompletion.create(
      model="gpt-4.1",
      messages=[
        {"role": "system", "content": "Você é um assistente de SQL."},
        {"role": "user", "content": prompt}
      ],
      max_tokens=150,
      temperature=0
    )

    # Extrai e limpa a resposta da API
    query = response['choices'][0]['message']['content'].strip()
    return query.replace("```sql", "").replace("```", "").strip()

  except openai.error.OpenAIError as e:
    # Captura erros específicos da API do OpenAI
    print(f"Erro ao chamar a API do OpenAI: {e}")
    return ""
  except Exception as e:
    # Captura qualquer outro erro que possa ocorrer
    print(f"Erro inesperado: {e}")
    return ""
