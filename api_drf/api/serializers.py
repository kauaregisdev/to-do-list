from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('"Title" field is required')
        if len(value) > 60:
            raise serializers.ValidationError('Title must not surpass 60 characters')
        return value
    
    def validate_description(self, value):
        if len(value) > 250:
            raise serializers.ValidationError('Description must not surpass 250 characters')
        return value