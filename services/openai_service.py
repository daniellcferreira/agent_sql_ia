import openai
import json
from utils.prompt_loader import carregar_prompt

# Função para gerar uma consulta SQL com base em uma pergunta em linguagem natural
def gerar_query_sql(pergunta, estrutura, api_key):
  openai.api_key = api_key  # Define a chave da API da OpenAI
  prompt = carregar_prompt()  # Carrega as instruções do prompt

  # Formata instruções adicionais
  instrucoes = "\n- " + "\n- ".join(prompt.get("instrucoes_sql", []))

  # Monta o contexto enviado para o modelo com base no prompt e na estrutura do banco
  contexto = f"""
  Sistema: {prompt.get("sistema_name", "Desconhecido")}
  Função do modelo: {prompt.get("model_role", "")}
  Perfil do usuario: {prompt.get("user_profile", {})}
  Restrições: {'; '.join(prompt.get("restricoes", {}))}
  Instruções adicionais:
  {instrucoes}
  Base de dados:
  {json.dumps(estrutura, indent=2, ensure_ascii=False)}
  Pergunta do usuário:
  {pergunta}
  """

  # Envia requisição para o modelo da OpenAI
  response = openai.ChatCompletion.create(
    model="gpt-4.1",
    messages=[
      {"role": "system", "content": prompt.get("model_role", "Você é um assistente de SQL.")},
      {"role": "user", "content": contexto}
    ],
    max_tokens=3000,
    temperature=0
  )

  # Retorna a query limpa (sem blocos de markdown)
  return response.choices[0].message.content.strip().replace("```sql", "").replace("```", "").strip()
