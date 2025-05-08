#!/bin/bash

# Função para ler senha de forma oculta
read_password() {
  local prompt=$1
  local password
  read -s -p "$prompt" password
  echo
  echo "$password"
}

# Verifica se o apt está disponível (para ambientes Linux ou WSL)
if ! command -v apt &> /dev/null
then
    echo "apt não encontrado. Verifique se está usando o WSL ou uma distribuição compatível."
    exit 1
fi

# Atualiza o apt
echo "Atualizando o apt..."
sudo apt update

# Instala o MySQL
echo "Instalando o MySQL..."
sudo apt install mysql-server -y

# Inicia o serviço do MySQL
echo "Iniciando o serviço do MySQL..."
sudo service mysql start

# Aguarda o MySQL iniciar
sleep 5

# Solicita senha para o root
root_password=$(read_password "Digite a senha desejada para o usuário 'root': ")

# Configura a senha do root
echo "Configurando a senha do usuário root..."
sudo mysql -u root <<EOF
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '${root_password}';
FLUSH PRIVILEGES;
EOF

# Solicita nome e senha para o novo usuário
read -p "Digite o nome do novo usuário: " new_user
new_user_password=$(read_password "Digite a senha para o usuário '${new_user}': ")

# Cria o novo usuário e concede permissões
echo "Criando o usuário '${new_user}'..."
sudo mysql -u root -p"${root_password}" <<EOF
CREATE USER '${new_user}'@'localhost' IDENTIFIED BY '${new_user_password}';
GRANT ALL PRIVILEGES ON *.* TO '${new_user}'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
EOF

echo "MySQL instalado e configurado com sucesso!"
echo "Usuário '${new_user}' criado com acesso total via localhost."
