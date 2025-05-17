from flask_sqlalchemy import SQLAlchemy # importando a função para usar banco de dados na API
from flask import Flask, Response, request, jsonify # importando as funções necessárias do Flask para a API
from functools import wraps # importando função para criar uma decorator
from datetime import datetime, UTC # importando função que retorna a data atual

USERNAME = 'admin'
PASSWORD = 'admin123'

def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response(
        'Access restricted.\n'
        'Provide valid username and password.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

class Task(db.Model): # cria um modelo de tarefa
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(250))
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC))

with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['POST']) # método que envia dados para a API
@requires_auth
def create_task(): # cria tarefa com nome, descrição e ID
    data = request.get_json()
    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({'error': '"Title" field is required'}), 400
    if len(data.get('title')) > 60:
        return jsonify({'error': 'Title must not surpass 60 characters'}), 400
    if len(data.get('description', '')) > 250:
        return jsonify({'error': 'Description must not surpass 250 characters'}), 400
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
        'created_at': new_task.created_at
    }), 201

@app.route('/tasks', methods=['GET']) # método que busca dados da API
@requires_auth
def read_tasks(): # retorna uma lista com as tarefas cadastrados
    tasks = Task.query.all()
    return jsonify([{
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'done': task.done,
            'created_at': task.created_at
        } for task in tasks]), 200

@app.route('/tasks/<int:task_id>', methods=['PUT']) # método que atualiza dados já existentes na API
@requires_auth
def update_task(task_id): # atualiza dados de uma tarefa específica
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Data was not provided'}), 400
    if 'title' in data and not data['title'].strip():
        return jsonify({'error': '"Title" field cannot be void'}), 400
    if 'title' in data and len(data['title']) > 60:
        return jsonify({'error': 'Title must not surpass 60 characters'}), 400
    if 'description' in data and len(data['description']) > 250:
        return jsonify({'error': 'Description must not surpass 250 characters'}), 400
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.done = data.get('done', task.done)
    db.session.commit()
    return jsonify({
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done,
        'updated_at': task.updated_at
    }), 200

@app.route('/tasks/<int:task_id>', methods=['DELETE']) # método que deleta dados de uma API
@requires_auth
def delete_task(task_id): # deleta uma tarefa específica
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True) # roda o servidor (usando waitress para rodar sem exceções)
