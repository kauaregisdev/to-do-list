from flask import Flask, request, jsonify # importando as funções necessárias do Flask para a API
from saves import *

app = Flask(__name__)

tasks = load_tasks() # onde serão armazenados os dados
next_id = max([task['id'] for task in tasks], default=0) + 1 # define o número do ID de cada tarefa

@app.route('/tasks', methods=['POST']) # método que envia dados para a API
def create_task(): # cria tarefa com nome, descrição e ID
    global next_id
    data = request.json
    if not data.get('title') or not data.get('description'): # checando se há nome e descrição
        return jsonify({'message': 'Name and description are required'}), 401
    data['id'] = next_id
    data['done'] = bool(data.get('done'))
    tasks.append(data)
    save_tasks(tasks)
    next_id += 1
    return jsonify(data), 201

@app.route('/tasks', methods=['GET']) # método que busca dados da API
def read_tasks(): # retorna uma lista com as tarefas cadastrados
    return jsonify(tasks), 200

@app.route('/tasks/<int:task_id>', methods=['PUT']) # método que atualiza dados já existentes na API
def update_task(task_id): # atualiza dados de uma tarefa específica
    data = request.json
    if not data.get('title') or not data.get('description'): # checando se há nome e descrição
        return jsonify({'message': 'Name and description are required'}), 401
    for task in tasks:
        if task['id'] == task_id:
            task['title'] = data['title']
            task['description'] = data['description']
            task['done'] = bool(data.get('done'))
            save_tasks(tasks)
            return jsonify(task), 200
    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE']) # método que deleta dados de uma API
def delete_task(task_id): # deleta uma tarefa específica
    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_tasks(tasks)
            return jsonify({'message': 'Task deleted'}), 204
    return jsonify({'message': 'Task not found'}), 404

if __name__ == '__main__':
    app.run(debug=True) # roda o servidor (usando waitress para rodar sem exceções)
