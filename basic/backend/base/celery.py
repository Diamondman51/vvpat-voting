from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from . import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

app = Celery('base')
app.conf.enable_utc = False
app.conf.update(timezone="Asia/Kolkata")

app.config_from_object(settings, namespace='CELERY')


app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
