from os import environ # importando função necessária pra retornar o endpoint do PostgreSQL
import jwt # importando a biblioteca do JSON Web Token
from flask_sqlalchemy import SQLAlchemy # importando a função para usar banco de dados na API
from flask import Flask, request, jsonify # importando as funções necessárias do Flask para a API
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

with app.app_context():
    db.drop_all()
    db.create_all()

from scripts.views import *

if __name__ == '__main__':
    app.run(debug=True) # roda o servidor (usando waitress para rodar sem exceções)
