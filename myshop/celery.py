import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

# Load task settings from Django settings with the namespace 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in installed apps
app.autodiscover_tasks()

# Set broker URL and result backend to use Redis
redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.conf.broker_url = redis_url
app.conf.result_backend = redis_url
