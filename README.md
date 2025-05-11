# QueryBank

[![Python](https://img.shields.io/badge/Python-linguagem-3572A5.svg?style=flat&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-framework-FF4F4F.svg?style=flat&logo=streamlit)](https://streamlit.io/)
[![MySQL](https://img.shields.io/badge/MySQL-banco%20de%20dados-4479A1.svg?style=flat&logo=mysql)](https://www.mysql.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-IA%20para%20SQL-0061F2.svg?style=flat&logo=openai)](https://openai.com/)

## Descrição

**dioBank Consultas** é um sistema interativo que permite aos usuários realizar consultas a um banco de dados MySQL utilizando linguagem natural. O sistema utiliza o poder da **OpenAI GPT-4** para converter perguntas em SQL de maneira eficiente. A interface do usuário é construída com **Streamlit**, proporcionando uma experiência intuitiva para quem deseja interagir com o banco de dados sem precisar saber SQL.

O projeto é ideal para analistas e usuários de bancos de dados que precisam extrair dados de maneira rápida e prática sem a complexidade de escrever comandos SQL manualmente.

## Funcionalidades

- **Geração Automática de SQL**: O sistema converte perguntas em linguagem natural para consultas SQL, simplificando a interação com o banco de dados. O modelo **OpenAI GPT-4** entende contextos e cria consultas que atendem às necessidades do usuário.
- **Interface Intuitiva com Streamlit**: A interface é feita com **Streamlit**, que permite a visualização interativa de dados. Usuários podem facilmente fazer perguntas, visualizar respostas e até fornecer feedback sobre as respostas geradas.
- **Armazenamento de Histórico**: O sistema mantém um histórico das interações, incluindo perguntas, consultas geradas, resultados e feedbacks. Isso permite melhorar a precisão das respostas e ter um acompanhamento de todas as consultas feitas.
- **Feedback do Usuário**: Após a execução das consultas, os usuários podem fornecer feedback sobre a utilidade das respostas, o que ajuda a melhorar o sistema ao longo do tempo. Este feedback é armazenado para aprimorar futuras interações.
- **Consultas Personalizadas**: O sistema permite que os usuários façam consultas personalizadas com base em suas necessidades. Não importa se você deseja dados de clientes, movimentações financeiras ou pagamentos, o **dioBank Consultas** torna tudo mais simples.

## Tecnologias Abordadas

- **Python 3.8+**: Linguagem de programação utilizada para o desenvolvimento do sistema. Com Python, foram desenvolvidas as funcionalidades principais do sistema, incluindo integração com **Streamlit** e **OpenAI GPT-4**.
- **Streamlit**: Framework utilizado para construir a interface do usuário. Com **Streamlit**, é possível criar dashboards interativos e amigáveis em questão de minutos, sem a necessidade de um front-end complexo.
- **OpenAI GPT-4**: O modelo de **IA** utilizado para interpretar perguntas em linguagem natural e convertê-las em consultas SQL. Com o **GPT-4**, é possível realizar tarefas de geração de SQL mais precisas e eficientes, com a capacidade de aprender e melhorar ao longo do tempo.
- **MySQL**: Sistema de gerenciamento de banco de dados utilizado para armazenar as informações bancárias e para executar as consultas SQL geradas pelo sistema. O MySQL é amplamente utilizado por sua robustez e flexibilidade em ambientes de produção.
- **dotenv**: Biblioteca que facilita o gerenciamento de variáveis de ambiente, como as chaves da API do **OpenAI** e as credenciais de acesso ao banco de dados. O uso do **dotenv** ajuda a manter as informações sensíveis seguras e bem organizadas.
- **JSON**: Utilizado para armazenar e carregar os prompts personalizados que o modelo **OpenAI** usa para gerar consultas SQL. O formato JSON torna a integração e a manutenção do sistema mais flexível.

