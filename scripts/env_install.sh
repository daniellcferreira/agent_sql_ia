#!/bin/bash

VERSION=$1
NOME_ENV=$2

# instala o pyenv e o virtualenv
brew install pyenv-virtualenv

# inicializa o pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# instala o python
pyenv install -s $VERSION
echo "Instalado o python $VERSION"

# cria o ambiente virtual
pyenv virtualenv $NOME_ENV $VERSION
echo "Criado o ambiente virtual $NOME_ENV"

# ativa o ambiente virtual
pyenv activate $NOME_ENV
echo "Ativado o ambiente virtual $NOME_ENV"

# instala as dependências
pip install -r requirements.txt
echo "Instaladas as dependências"  
