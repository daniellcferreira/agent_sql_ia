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