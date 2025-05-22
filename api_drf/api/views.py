from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task

def bad_request(request, exception):
    return JsonResponse({'error': 'Bad Request', 'message': str(exception)}, status=400)

def forbidden(request, exception):
    return JsonResponse({'error': 'Forbidden', 'message': str(exception)}, status=403)

def not_found(request, exception):
    return JsonResponse({'error': 'Not Found', 'message': str(exception)}, status=404)

def internal_error(request):
    return JsonResponse({'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}, status=500)

class TasksView(APIView):
    def post(self, request):
        ...
        
    def get(self, request):
        ...

    def put(self, request, task_id):
        ...

    def delete(self, request, task_id):
        ...
