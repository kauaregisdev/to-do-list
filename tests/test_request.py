# este código testa a API criada em app.py
import requests

url = 'http://127.0.0.1:8080/login'
json = {
    'username': 'admin',
    'password': 'admin123'
}

response = requests.post(url, json=json)
headers = response.json()
print('POST /tasks', headers)

url = 'http://127.0.0.1:8080/tasks'
json = {
    'title': 'Study Django',
    'description': 'Learn the basics of Django framework for Python',
}

response = requests.post(url, json=json, headers=headers)
print('POST /tasks:', response.json())

response = requests.get(url, headers=headers)
print('GET /tasks:', response.json())

url = 'http://127.0.0.1:8080/tasks/1'
json = {
    'title': 'Study Flask',
    'description': 'Learn the basics of Flask framework for Python',
    'done': 1
}

response = requests.put(url, json=json, headers=headers)
print('PUT /tasks:', response.json())

response = requests.delete(url, headers=headers)
if response.content:
    print('DELETE /tasks:', response.json())
else:
    print('DELETE /tasks:', response.status_code)
