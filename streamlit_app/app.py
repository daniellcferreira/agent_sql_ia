import streamlit as st
from ui.sidebar import carregar_credenciais
from utils.schema_inspector import obter_estruturas_tabelas
from services.openai_service import gerar_query_sql
from services.database_service import executar_query_sql, salvar_historico, salvar_feedback

# Configuração da página
st.set_page_config(page_title="dioBank Consultas")
st.title("dioBank Consultas")

# Carrega credenciais da sidebar
creds = carregar_credenciais()

# Inicializa variável de sessão
if "pergunta" not in st.session_state:
  st.session_state.pergunta = ""

# Seção de sugestões de perguntas
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

# Campo de pergunta personalizada
st.markdown("### Pergunta personalizada")
pergunta = st.text_input("Digite sua pergunta:", value=st.session_state.pergunta, key="input_pergunta")

if pergunta:
  # Obtém estrutura das tabelas
  estrutura = obter_estruturas_tabelas(creds)

  if estrutura:
    # Gera query SQL a partir da pergunta
    query = gerar_query_sql(pergunta, estrutura, creds["openai_api_key"])

    # Exibe a query SQL se usuário quiser
    if st.toggle("Mostrar consulta SQL"):
      st.code(query, language="sql")

    # Executa a query no banco e exibe os resultados
    colunas, resultados = executar_query_sql(query, creds)

    if resultados:
      st.success("Consulta executada com sucesso!")
      st.dataframe([dict(zip(colunas, linha)) for linha in resultados])

      # Salva pergunta, query e resultado no histórico
      salvar_historico(pergunta, query, resultados, creds)
    else:
      st.warning("Nenhum resultado encontrado.")

    # Feedback do usuário sobre a resposta
    feedback = st.radio("Essa resposta foi útil?", ("Sim", "Nao"))
    salvar_feedback(pergunta, feedback, creds)
