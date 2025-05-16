from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify # importando as funções necessárias do Flask para a API

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model): # cria um modelo de tarefa
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(250))
    done = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all() # define o número do ID de cada tarefa

@app.route('/tasks', methods=['POST']) # método que envia dados para a API
def create_task(): # cria tarefa com nome, descrição e ID
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description', ''),
        done=data.get('done', False)
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'done': new_task.done,
    }), 201

@app.route('/tasks', methods=['GET']) # método que busca dados da API
def read_tasks(): # retorna uma lista com as tarefas cadastrados
    tasks = Task.query.all()
    return jsonify([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'done': task.done,
        } for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['PUT']) # método que atualiza dados já existentes na API
def update_task(task_id): # atualiza dados de uma tarefa específica
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done,
    })

@app.route('/tasks/<int:task_id>', methods=['DELETE']) # método que deleta dados de uma API
def delete_task(task_id): # deleta uma tarefa específica
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True) # roda o servidor (usando waitress para rodar sem exceções)
