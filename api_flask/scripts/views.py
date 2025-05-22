from scripts.main import app, db, generate_token, requires_jwt, USERNAME, PASSWORD
from scripts.models import Task
from flask import abort, request, jsonify

def task_to_dict(task):
    return{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done,
        'created_at': task.created_at.isoformat() if task.created_at else None,
        'updated_at': task.updated_at.isoformat() if task.updated_at else None
    }

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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if username == USERNAME and password == PASSWORD:
        token = generate_token(username)
        return jsonify({'Authorization': 'Bearer '+token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/tasks', methods=['POST']) # método que envia dados para a API
@requires_jwt
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
@requires_jwt
def read_tasks(): # retorna uma lista com as tarefas cadastrados
    page = request.args.get('page', 1, type=int)
    per_page = 5
    pagination = Task.query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = [task_to_dict(task) for task in pagination.items]
    return jsonify({
        'tasks': tasks,
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'per_page': pagination.per_page
    }), 200

@app.route('/tasks/<int:task_id>', methods=['PUT']) # método que atualiza dados já existentes na API
@requires_jwt
def update_task(task_id): # atualiza dados de uma tarefa específica
    task = db.session.get(Task, task_id)
    if not task:
        abort(404)
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
@requires_jwt
def delete_task(task_id): # deleta uma tarefa específica
    task = db.session.get(Task, task_id)
    if not task:
        abort(404)
    db.session.delete(task)
    db.session.commit()
    return ('', 204)