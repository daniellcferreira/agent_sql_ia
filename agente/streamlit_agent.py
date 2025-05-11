import streamlit as st
import mysql.connector
import openai
import os
from dotenv import load_dotenv
import json

load_dotenv()

# configuração da página streamlit

st.set_page_config(page_title="dioBank Consultas")
st.title("dioBank Consultas")

# sidebar para credenciais
st.sidebar.header("Configurações")
openai_api_key = st.sidebar.text_input("Chave de API OpenAI", type="password")
mysql_host = st.sidebar.text_input("MySQL Host", value="localhost")
mysql_user = st.sidebar.text_input("Usuário MySQL", value="root")
mysql_password = st.sidebar.text_input("Senha MySQL", type="password")
mysql_db = st.sidebar.text_input("Nome do Banco de Dados", value="dioBank")

# sessão para mandar pergunta sugerida
if "pergunta" not in st.session_state:
  st.session_state.pergunta = ""

# sugestões de perguntas como no GPT
st.markdown("### Sugestões de perguntas")
col1, col2, col3, col4 = st.columns(4)
with col1:
  if st.button("Clientes"):
    st.session_state.pergunta = "Me mostre todos os clientes"
with col2:
  if st.button("Pagamentos"):
    st.session_state.pergunta = "Me mostre todos os pagamentos"
with col3:
  if st.button("Endereços"):
    st.session_state.pergunta = "Me mostre todos os endereços"
with col4:
  if st.button("Movimentações"):
    st.session_state.pergunta = "Me mostre todas as movimentações"

# campo de pergunta
st.markdown("### Pergunta personalizada")
pergunta = st.text_input("Digite sua pergunta em linguagem natural:", 
                         value=st.session_state.pergunta, 
                         key="input_pergunta")

# função para obter estrutura das tabelas
def obter_estruturas_tabelas():
  try:
    conn = mysql.connector.connect(
      host=mysql_host,
      user=mysql_user,
      password=mysql_password,
      database=mysql_db
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
    st.error(f"Erro ao conectar ao banco de dados: {e}")
    return {}
  
# função para carregar o prompt salvo
def carregar_prompt():
  try:
    with open("config/prompt.json", "r", encoding="utf-8") as f:
      return json.load(f)
  except Exception as e:
    st.error(f"Erro ao carregar o prompt: {e}")
    return {}
  
# função para gerar a query SQL
def gerar_query_sql(question, columns):
  openai.api_key = (openai_api_key)
  prompt = carregar_prompt()

  instrucoes_adicionais = "\n- " + "\n- ".join(prompt.get("instrucoes_sql", []))

  contexto = f"""
    Sistema: {prompt.get("sistema_name", "Desconhecido")}
    Função do modelo: {prompt.get("model_role", "")}
    Perfil do usuario: {prompt.get("user_profile", {})}
    Restrições: {'; '.join(prompt.get("restricoes", {}))}

    Intruções adicionais:
    {instrucoes_adicionais}

    Base de dados:
    {json.dumps(columns, indent=2, ensure_ascii=False)}

    Pergunta do usuário:
    {question}   
  """

  try:
    response = openai.ChatCompletion.create(
      model="gpt-4.1",
      messages=[
        {"role": "system", "content": prompt.get("model_role", "Você é um assistente de SQL.")},
        {"role": "user", "content": contexto}
      ],
      max_tokens=3000,
      temperature=0
    )
    query = response.choices[0].message.content.strip()
    return query.replace("```sql", "").replace("```", "").strip()
  except Exception as e:
    st.error(f"Erro ao gerar a query SQL: {e}")
    return ""
  
# função para executar a query SQL
def executar_query_sql(query):
  if not query:
    st.warning("A consuta SQL está vazia. Verifique se a pergunta foi formulada corretamente.")
  try:
    conn = mysql.connector.connect(
      host=mysql_host,
      user=mysql_user,
      password=mysql_password,
      database=mysql_db
    )
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    cursor.close()
    conn.close()
    return result, columns
  except Exception as e:
    st.error(f"Erro ao executar a query SQL: {e}")
    return [], []
  
# função para salvar histórico de perguntas e respostas
def salvar_historico(question, query, result):
  try:
    conn = mysql.connector.connect(
      host=mysql_host,
      user=mysql_user,
      password=mysql_password,
      database=mysql_db
    )
    cursor = conn.cursor()

    # garantir criação e tipo correto da tabela
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
    """, (question, query, result))
    conn.commit()
    cursor.close()
    conn.close()
  except Exception as e:
    st.error(f"Erro ao salvar histórico: {e}")

# função para salvar feedback do usuário
def salvar_feedback(question, feedback):
  try:
    conn = mysql.connector.connect(
      host=mysql_host,
      user=mysql_user,
      password=mysql_password,
      database=mysql_db
    )
    cursor = conn.cursor()
    cursor.execute("""
      UPDATE historico_interacoes
      SET feedback = %s
      WHERE pergunta = %s
      ORDER BY data DESC LIMIT 1;         ;
    """, (question, feedback))
    conn.commit()
    cursor.close()
    conn.close()
  except Exception as e:
    st.error(f"Erro ao salvar feedback: {e}")

# execução principal
if pergunta:
  estrutura = obter_estruturas_tabelas()
  if estrutura:
    query = gerar_query_sql(pergunta, estrutura)

    mostrar_sql = st.toggle("Mostrar consulta SQL")
    if mostrar_sql:
      st.code(query, language="sql")

    colunas, resultados = executar_query_sql(query)

    if resultados:
      st.success("Consulta executada com sucesso!")
      st.dataframe([dict(zip(colunas, linha)) for linha in resultados])
      salvar_historico(pergunta, query, resultados)
    else:
      st.warning("Nenhum resultado encontrado para esta consulta.")

    feedback = st.radio("Essa resposta foi util?", ("Sim", "Nao"), key="feedback")
    salvar_feedback(pergunta, feedback)