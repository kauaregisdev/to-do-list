# este código testa a API criada em app.py
import requests

url = 'http://127.0.0.1:5000/tasks'
json = {
    'title': 'Study Django',
    'description': 'Learn the basics of Django framework for Python',
}
user_url = 'http://127.0.0.1:5000/tasks/1'
new_json = {
    'title': 'Study Flask',
    'description': 'Learn the basics of Flask framework for Python',
    'done': 1
}
auth = ('admin', 'admin123')

response = requests.post(url, json=json, auth=auth)
print('POST /tasks:', response.json())

response = requests.get(url, auth=auth)
print('GET /tasks:', response.json())

response = requests.put(user_url, json=new_json, auth=auth)
print('PUT /tasks:', response.json())

response = requests.delete(user_url, auth=auth)
if response.content:
    print('DELETE /tasks:', response.json())
else:
    print('DELETE /tasks:', response.status_code)