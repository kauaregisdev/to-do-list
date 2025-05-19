import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pytest import fixture
from scripts.app import app, db
os.environ['DATABASE_URL'] = 'postgresql://admin:admin123@localhost:5432/to_do_list_test'

@fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client

def get_token(client):
    response = client.post('/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    assert response.status_code == 200 or response.status_code == 201
    data = response.get_json()
    return data['Authorization']

def auth_header(token):
    return {'Authorization': token}

def test_create_task_success(client):
    token = get_token(client)
    response = client.post('/tasks', json={
        'title': 'Study Flask',
        'description': 'Learn Flask framework for Python',
        'done': False
    }, headers=auth_header(token))
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Study Flask'
    assert 'created_at' in data

def test_tasks_pagination(client):
    token = get_token(client)
    for i in range(12):
        client.post('/tasks', json={
            'title': f'Task {i}',
            'description': f'Description {i}'
        }, headers=auth_header(token))
    response = client.get('/tasks?page=1', headers=auth_header(token))
    assert response.status_code == 200
    data = response.get_json()
    assert data['page'] == 1
    assert data['per_page'] == 5
    assert data['total'] == 12
    assert data['pages'] == 3
    assert len(data['tasks']) == 5

def test_update_task_success(client):
    token = get_token(client)
    post = client.post('/tasks', json={'title': 'Study PHP'}, headers=auth_header(token))
    task_id = post.get_json()['id']
    response = client.put(f'/tasks/{task_id}', json={'done': True}, headers=auth_header(token))
    assert response.status_code == 200
    data = response.get_json()
    assert data['done'] is True

def test_delete_task_success(client):
    token = get_token(client)
    post = client.post('/tasks', json={'title': 'Study Java'}, headers=auth_header(token))
    task_id = post.get_json()['id']
    response = client.delete(f'/tasks/{task_id}', headers=auth_header(token))
    assert response.status_code == 204

def test_create_task_missing_title(client):
    token = get_token(client)
    response = client.post('/tasks', json={'description': 'Something'}, headers=auth_header(token))
    assert response.status_code == 400
    assert '"Title" field is required' in response.get_json()['error']

def test_create_task_title_too_long(client):
    token = get_token(client)
    task_title = 'a' * 61
    response = client.post('/tasks', json={'title': task_title}, headers=auth_header(token))
    assert response.status_code == 400
    assert 'Title must not surpass 60 characters' in response.get_json()['error']

def test_create_task_desc_too_long(client):
    token = get_token(client)
    task_desc = 'a' * 251
    response = client.post('/tasks', json={'title': 'Something', 'description': task_desc}, headers=auth_header(token))
    assert response.status_code == 400
    assert 'Description must not surpass 250 characters' in response.get_json()['error']

def test_update_task_not_found(client):
    token = get_token(client)
    response = client.put('/tasks/9999', json={'title': 'Title'}, headers=auth_header(token))
    assert response.status_code == 404

def test_update_task_not_data(client):
    token = get_token(client)
    post = client.post('/tasks', json={'title': 'Something', 'description': 'Something else'}, headers=auth_header(token))
    task_id = post.get_json()['id']
    response = client.put(f'/tasks/{task_id}', json={}, headers=auth_header(token))
    assert response.status_code == 400
    assert 'Data was not provided' in response.get_json()['error']

def test_update_task_void_title(client):
    token = get_token(client)
    post = client.post('/tasks', json={'title': 'Something', 'description': 'Something else'}, headers=auth_header(token))
    task_id = post.get_json()['id']
    response = client.put(f'/tasks/{task_id}', json={'title': ''}, headers=auth_header(token))
    assert response.status_code == 400

def test_update_task_title_too_long(client):
    token = get_token(client)
    post = client.post('/tasks', json={'title': 'Something'}, headers=auth_header(token))
    task_id = post.get_json()['id']
    task_title = 'a' * 61
    response = client.put(f'/tasks/{task_id}', json={'title': task_title}, headers=auth_header(token))
    assert response.status_code == 400
    assert 'Title must not surpass 60 characters' in response.get_json()['error']

def test_update_task_desc_too_long(client):
    token = get_token(client)
    post = client.post('/tasks', json={'title': 'Something'}, headers=auth_header(token))
    task_id = post.get_json()['id']
    task_desc = 'a' * 251
    response = client.put(f'/tasks/{task_id}', json={'description': task_desc}, headers=auth_header(token))
    assert response.status_code == 400
    assert 'Description must not surpass 250 characters' in response.get_json()['error']

def test_delete_task_not_found(client):
    token = get_token(client)
    response = client.delete('/tasks/9999', headers=auth_header(token))
    assert response.status_code == 404

def test_access_without_token(client):
    response = client.get('/tasks')
    assert response.status_code == 401
    assert 'Token missing' in response.get_json()['error']

def test_access_with_invalid_token(client):
    response = client.get('/tasks', headers={'Authorization': 'Bearer token_invalido'})
    assert response.status_code == 401
    assert 'Invalid or expired token' in response.get_json()['error']