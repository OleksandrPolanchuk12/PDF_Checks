from __future__ import absolute_import
import celery, os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Issuing_checks.settings')
app = celery.Celery('issuing_checks')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()