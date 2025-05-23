import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'api_drf.settings'
)
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_user(username='admin', password='admin123')
    print('User created.')
else:
    print('User already exists.')