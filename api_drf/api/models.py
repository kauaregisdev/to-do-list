from django.db import models

class TaskDRF(models.Model): # cria um modelo de tarefa
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=60)
    description = models.TextField(max_length=250, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
