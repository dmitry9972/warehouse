from celery import Celery
import requests
import json
from django.template.loader import render_to_string
from django.conf import settings
import logging
from celery import Task
from carriers.cdek import CDEK

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")

app = Celery('tasks', broker=settings.WAREHOUSE_REDIS_BROKER)






CDEK_task=app.register_task(CDEK( settings.CDEK_LOGIN,
                                     settings.CDEK_PASSWORD ))


