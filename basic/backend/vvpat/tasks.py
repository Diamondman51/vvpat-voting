from celery import shared_task
from time import sleep
from django.core.cache import cache

@shared_task
def set_timer():
    print("Timer: ", cache.get('timer'))
    cache.set('timer', False, 60*60*18)