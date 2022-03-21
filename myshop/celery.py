import os 
from celery import Celery

"""
Set DJANGO_SETTINGS_MODULE variable for the Celerey
Create instance aplication, app = Celery('myshop')
Load custome configuration from settings
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()