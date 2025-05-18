# Celery configuration file

import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_process.settings')

# Create the Celery app
app = Celery('data_process')

# Use a string here to avoid pickle serialization issues
app.config_from_object('django.conf:settings', namespace='CELERY')

# Configure broker URL with fallback for backward compatibility
app.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://data_redis:6379/0')
app.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND', 'redis://data_redis:6379/0')

# Configure Celery to retry if connection is lost
app.conf.broker_connection_retry = True
app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 10
app.conf.broker_connection_timeout = 10

# Using json for serialization
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']

# Auto-discover tasks from installed apps
app.autodiscover_tasks()

# For debugging
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
