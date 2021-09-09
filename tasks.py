from celery import Celery
import requests
import json
from django.template.loader import render_to_string
from django.conf import settings
import logging

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")

app = Celery('tasks', broker='redis://localhost:6379/1')


@app.task
def send_order_to_cdec(data_to_transfer, order_pk):
    from main.models import Order

    def register_to_cdec():
        Account = 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI'
        Secure_password = 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'
        url = 'https://api.edu.cdek.ru/v2/oauth/token?parameters'
        payload = {'grant_type': 'client_credentials',
                   'client_id': Account,
                   'client_secret': Secure_password,
                   }
        r = requests.post(url, data=payload)

        cdec_response = json.loads(r.text)

        if settings.DEBUG == True:
            logger = logging.getLogger(__name__)
            logger.warning('access_token:')
            logger.warning(cdec_response['access_token'])

        token = cdec_response['access_token']
        return token

    def transfer_to_cdec(token, data_to_transfer):
        url = 'https://api.edu.cdek.ru/v2/orders'
        headers = {'Authorization': 'Bearer {}'.format(token)}

        order_comment = "Order N{order_num} at {order_date}".format(
            order_num=data_to_transfer['order_pk'],
            order_date=data_to_transfer['order_date']
        )


        if settings.DEBUG == True:
            logger = logging.getLogger(__name__)
            logger.warning('order_info:')
            logger.warning(data_to_transfer['order_info'])


        json_data_to_transfer = json.loads(data_to_transfer['order_info'])
        products = ''
        products += 'From ' + json_data_to_transfer['1']['username'] + ':'
        for m in json_data_to_transfer:
            products += json_data_to_transfer[m]['product_name'] + ':'
            products += str(json_data_to_transfer[m]['product_count']) + '; '

        context = {'comment': order_comment,
                   'products': products,
                   'sender_name': json_data_to_transfer['1']['username']}

        data_send = render_to_string('json_templates/cdek_create_order.txt', context)
        encoded_data = data_send.encode('utf-8')


        cdek_json = json.loads(encoded_data)

        r = requests.post(url, json=cdek_json, headers=headers)


        if settings.DEBUG == True:
            logger = logging.getLogger(__name__)
            logger.warning('r.text:')
            logger.warning(r.text)


        entity_uuid = json.loads(r.text)['entity']['uuid']


        return entity_uuid

    def save_uuid_to_model(order_uuid):
        m = Order.objects.get(pk=order_pk)
        m.cdek_uuid = order_uuid
        m.save()

        if settings.DEBUG == True:
            logger = logging.getLogger(__name__)
            logger.warning('UUID SAVED: ')
            logger.warning(order_uuid)




    def send_uuid_to_shop(order_uuid):


        headers = {'Authorization': 'Token 8e58ec44038ab7947bfb07e55f2c6fd2ded2a311'}

        m = Order.objects.get(pk=order_pk)
        send_order_number = m.order_number
        url = 'http://127.0.0.1:8000/api/order/update/{}/'.format(send_order_number)


        data_send = {'cdek_uuid': order_uuid  ,
                     'status': 2}
        r = requests.patch(url, data=data_send, headers=headers)


        if settings.DEBUG == True:
            logger = logging.getLogger(__name__)
            logger.warning('r.text: ')
            logger.warning(r.text)
            logger.warning('UUID SENT TO SHOP - warehouse pk: ')
            logger.warning(order_pk)
            logger.warning('UUID SENT TO SHOP - shop pk: ')
            logger.warning(send_order_number)




    if settings.DEBUG == True:
        logger = logging.getLogger(__name__)
        logger.warning('WAREHOUSE ENTER')

    token = register_to_cdec()
    order_uuid = transfer_to_cdec(token=token, data_to_transfer=data_to_transfer);
    save_uuid_to_model(order_uuid)
    send_uuid_to_shop(order_uuid)



    return
