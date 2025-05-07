from __future__ import absolute_import,unicode_literals
import os

from celery import Celery 
from django.conf import settings 
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','stock_tracker.settings')

app=Celery('stock_tracker')
app.conf.enable_utc=False
app.conf.update(timezone='Asia/Kolkata')
app.config_from_object(settings,namespace='CELERY')

app.conf.beat_schedule = {
    # 'every-10-seconds' : {
    #     'task': 'mainapp.tasks.update_stock',
    #     'schedule': 10,
    #     'args': (['APPL','SAP'],)
    # },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request :{self.request!r}')