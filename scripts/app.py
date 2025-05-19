from os import environ
import jwt # importando a biblioteca do JSON Web Token
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy # importando a função para usar banco de dados na API
from flask import Flask, abort, request, jsonify # importando as funções necessárias do Flask para a API
from functools import wraps # importando função para criar uma decorator
from datetime import timedelta, datetime, UTC # importando função que retorna a data atual

USERNAME = 'admin'
PASSWORD = 'admin123'
SECRET_KEY = 'ILgZzD9niA;b2bf'

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.now(UTC) + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
        return payload['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def requires_jwt(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Token missing'}), 401
        token = auth_header.split(' ')[1]
        username = verify_token(token)
        if not username:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get(
    'DATABASE_URL',
    'postgresql://admin:admin123@localhost:5000/to_do_list'
)
db = SQLAlchemy(app)
api = Api(app, title='To-do List API', description='Task management API')

task_model = api.model('Task', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True, max_length=60),
    'description': fields.String(max_length=250),
    'done': fields.Boolean,
    'created_at': fields.String,
    'updated_at': fields.String
})

@api.route('/tasks')
class TaskListResource(Resource):
    @api.doc('list_tasks')
    @api.marshal_list_with(task_model)
    def get(self):
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
    
    @api.doc('create_task')
    @api.expect(task_model)
    @api.marshal_with(task_model, code=201)
    def post(self):
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
    
@api.route('/tasks/<int:task_id>')
class TaskResource(Resource):
    @api.doc('update_task')
    @api.expect(task_model)
    @api.marshal_with(task_model)
    def put(self, task_id):
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
    
    @api.doc('delete_task')
    def delete(self, task_id):
        task = db.session.get(Task, task_id)
        if not task:
            abort(404)
        db.session.delete(task)
        db.session.commit()
        return ('', 204)

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

def task_to_dict(task):
    return{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'done': task.done,
        'created_at': task.created_at.isoformat() if task.created_at else None,
        'updated_at': task.updated_at.isoformat() if task.updated_at else None
    }

with app.app_context():
    db.drop_all()
    db.create_all()

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

if __name__ == '__main__':
    app.run(debug=True) # roda o servidor (usando waitress para rodar sem exceções)
