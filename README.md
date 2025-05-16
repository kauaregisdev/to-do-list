# To-do list (lista de tarefas)
Bem-vindo! Este projeto consiste numa API que gerencia uma lista de tarefas. Ela foi criada em Python, com o uso do framework Flask e de algumas bibliotecas.

## Status:
Funcionando, porém sujeito a receber novas implementações com o tempo. O projeto possui integração com SQLite para armazenamento de dados, roda num ambiente virtual e utiliza a biblioteca Waitress para dar deploy no servidor da API. No entanto, não foi feito ainda um sistema de checagem dos dados, ou mesmo de tratamento mais robusto de erros.

## Pré-requisitos:
Python 3.13
Ambiente virtual (recomendado)
Bibliotecas (para baixá-las, pip install -r requirements.txt)

## Como executar o código:
1. clone o repositório, executando no terminal os seguintes comandos:
git clone https://github.com/kauaregisdev/to-do-list.git
cd to-do-list

2. crie e ative o ambiente virtual, com os comandos:
python -m venv venv
venv\Scripts\Activate
OBSERVAÇÃO: caso haja uma pasta venv/ nos arquivos do projeto, delete-a antes de criar um novo ambiente virtual!

3. instale as dependências pelo terminal, com o comando:
pip install -r requirements.txt

4. execute o app Flask, com o comando:
cd scripts
waitress-serve --port=5000 app:app

5. rode os scripts de teste em outro terminal, com o comando:
cd scripts
python test_request.py (teste usando a biblioteca requests)
pytest test_auto.py (teste automatizado usando pytest)

OU, SE POSSÍVEL:
faça as requisições HTTP direto do Postman ou do Postcode, com a URL:
http://127.0.0.1:5000/tasks
para editar uma tarefa isolada, adicionar "/" e o ID da tarefa.
EX.: http://127.0.0.1:5000/tasks/1, para editar a tarefa cujo ID é 1.

Em breve farei uma documentação mais profunda da API como um todo.

## Observações importantes:
1. A API usa SQLite para armazenar os dados, mas pretendo evoluir esse serviço de banco de dados futuramente
2. O projeto, apesar de estar funcionando, está sujeito a sofrer alterações e implementações de novas funções no futuro