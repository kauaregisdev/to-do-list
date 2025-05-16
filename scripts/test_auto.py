import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_task(client):
    response = client.post('/tasks', json={
        'title': 'Study Flask',
        'description': 'Learn Flask framework for Python',
        'done': False
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Study Flask'
    assert 'created_at' in data

def test_get_tasks(client):
    client.post('/tasks', json={'title': 'Study Django'})
    response = client.get('/tasks')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_update_task(client):
    post = client.post('/tasks', json={'title': 'Study PHP'})
    task_id = post.get_json()['id']
    response = client.put(f'/tasks/{task_id}', json={'done': True})
    assert response.status_code == 200
    data = response.get_json()
    assert data['done'] is True

def test_delete_task(client):
    post = client.post('/tasks', json={'title': 'Study Java'})
    task_id = post.get_json()['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204