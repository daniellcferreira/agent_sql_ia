import json

# Função para carregar o prompt a partir de um arquivo JSON
def carregar_prompt():
  try:
    with open("config/prompt.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception:
    # Retorna um dicionário vazio caso ocorra algum erro (ex: arquivo não encontrado)
    return {}
