from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LoginView(APIView):
    def post(self, request):
        ...

class TasksView(APIView):
    def post(self, request):
        ...
        
    def get(self, request):
        ...

    def put(self, request, task_id):
        ...

    def delete(self, request, task_id):
        ...
