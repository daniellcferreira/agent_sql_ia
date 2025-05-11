import streamlit as st

# Função para carregar credenciais a partir da barra lateral do Streamlit
def carregar_credenciais():
  st.sidebar.header("Configurações")

  # Campos de entrada de credenciais
  return {
    "openai_api_key": st.sidebar.text_input("Chave de API OpenAI", type="password"),
    "mysql_host": st.sidebar.text_input("MySQL Host", value="localhost"),
    "mysql_user": st.sidebar.text_input("Usuário MySQL", value="root"),
    "mysql_password": st.sidebar.text_input("Senha MySQL", type="password"),
    "mysql_db": st.sidebar.text_input("Nome do Banco de Dados", value="dioBank")
  }
