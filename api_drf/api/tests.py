from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class GetTokenAPITest(TestCase):
    def test_get_token_success(self):
        User.objects.create_user(username='admin', password='admin123')
        url = reverse('token_obtain')
        response = self.client.post(url, {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.json())
        self.assertIn('access', response.json())

    def test_refresh_token_success(self):
        User.objects.create_user(username='admin', password='admin123')
        url = reverse('token_obtain')
        response = self.client.post(url, {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        refresh = response.json()['refresh']
        url = reverse('token_refresh')
        response = self.client.post(url, {
            'refresh': refresh
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.json())

class CreateTaskAPITest(TestCase):
    def test_create_task_success(self):
        User.objects.create_user(username='admin', password='admin123')
        url = reverse('token_obtain')
        response = self.client.post(url, {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        headers = {
            'authorization': f'Bearer {response.json()['access']}'
        }
        url = reverse('task_create')
        response = self.client.post(url, {
            'title': 'Study Django',
            'description': 'Learn about Django framework for Python'
        }, headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json())
        self.assertIn('title', response.json())
        self.assertIn('description', response.json())
        self.assertIn('done', response.json())
        self.assertIn('created_at', response.json())

class ListTasksAPITest(TestCase):
    def test_list_tasks_success(self):
        User.objects.create_user(username='admin', password='admin123')
        url = reverse('token_obtain')
        response = self.client.post(url, {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        headers = {
            'authorization': f'Bearer {response.json()['access']}'
        }
        url = reverse('task_create')
        for i in range(12):
            response = self.client.post(url, {
                'title': 'Study Django',
                'description': 'Learn about Django framework for Python'
            }, headers=headers, content_type='application/json')
        url = reverse('task_list')
        response = self.client.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('count', response.json())
        self.assertIn('next', response.json())
        self.assertIn('previous', response.json())
        self.assertIn('results', response.json())

class EditTaskAPITest(TestCase):
    def test_update_task_success(self):
        User.objects.create_user(username='admin', password='admin123')
        url = reverse('token_obtain')
        response = self.client.post(url, {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        headers = {
            'authorization': f'Bearer {response.json()['access']}'
        }
        url = reverse('task_create')
        response = self.client.post(url, {
            'title': 'Study Django',
            'description': 'Learn about Django framework for Python'
        }, headers=headers, content_type='application/json')
        url = reverse('task_detail', kwargs={'task_id': response.json()['id']})
        response = self.client.put(url, {
            'title': 'Study Node.js',
            'description': 'Learn about Node.js and its functions',
            'done': 1
        }, headers=headers, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('id', response.json())
        self.assertIn('title', response.json())
        self.assertIn('description', response.json())
        self.assertIn('done', response.json())
        self.assertIn('updated_at', response.json())

    def test_delete_task_success(self):
        User.objects.create_user(username='admin', password='admin123')
        url = reverse('token_obtain')
        response = self.client.post(url, {
            'username': 'admin',
            'password': 'admin123'
        }, content_type='application/json')
        headers = {
            'authorization': f'Bearer {response.json()['access']}'
        }
        url = reverse('task_create')
        response = self.client.post(url, {
            'title': 'Study Django',
            'description': 'Learn about Django framework for Python'
        }, headers=headers, content_type='application/json')
        url = reverse('task_detail', kwargs={'task_id': response.json()['id']})
        response = self.client.delete(url, headers=headers)
        self.assertEqual(response.status_code, 204)
