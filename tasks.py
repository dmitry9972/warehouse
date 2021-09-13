from celery import Celery
from celery.schedules import crontab
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


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(7.0, carrier_sheduler.s(), name='send to carrier every 7')


def prepare_data_for_carrier(order_pk):
    from main.models import Order
    import main.const
    order = Order.objects.get(pk=order_pk)

    transfer_data = {}
    transfer_data['order_client'] = order.order_client
    transfer_data['order_pk'] = order.pk
    transfer_data['order_date'] = order.order_date
    transfer_data['order_info'] = order.order_info
    return transfer_data


@app.task
def carrier_sheduler():

    from main.models import Order
    import main.const
    orders_to_push = Order.objects.filter(status=main.const.PROCESSING_ORDER)
    for m in orders_to_push:
        logger = logging.getLogger(__name__)
        logger.warning(m.pk)
        logger.warning(m.status)
        push_order_to_carrier.delay(prepare_data_for_carrier(m.pk), m.pk)


@app.task
def push_order_to_carrier(transfer_data, order_pk, carrier_name='CDEK'):

    from main.models import Order
    import main.const

    CDEK_instance = CDEK(settings.CDEK_LOGIN,
                         settings.CDEK_PASSWORD)
    CDEK_instance.send_order_to_cdec(transfer_data, order_pk)

    order = Order.objects.get(pk=order_pk)
    order.status = main.const.ORDER_SENT_TO_CARRIER
    order.save()
    return
