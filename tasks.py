from celery import Celery
import requests
import json
from django.template.loader import render_to_string
from django.conf import settings

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")

app = Celery('tasks', broker='redis://localhost:6379/1')


@app.task
def send_order_to_cdec(data_to_transfer):
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

        print(cdec_response['access_token'])

        token = cdec_response['access_token']
        return token

    def transfer_to_cdec(token, data_to_transfer):
        url = 'https://api.edu.cdek.ru/v2/orders'
        headers = {'Authorization': 'Bearer {}'.format(token)}

        # "comment": {{comment}}, - insert
        # order
        # number
        # here
        # "name": "{{ products }}", - inserd
        # products
        # here
        # "name": "{{ sender_name }}" - inser
        # user
        # name
        # here

        # transfer_data['order_client'] = order.order_client
        # transfer_data['order_pk'] = order.pk
        # transfer_data['order_date'] = order.order_date
        # transfer_data['order_info'] = order.order_info

        order_comment ="Order N{order_num} at {order_date}".format(
            order_num = data_to_transfer['order_pk'],
            order_date= data_to_transfer['order_date']
        )

        print(data_to_transfer['order_info'])
        json_data_to_transfer = json.loads(data_to_transfer['order_info'])
        products = ''
        products += 'From ' + json_data_to_transfer['1']['username'] + ':'
        for m in json_data_to_transfer:
            products += json_data_to_transfer[m]['product_name'] + ':'
            products += str(json_data_to_transfer[m]['product_count']) + '; '

        print(products)

        context = {'comment': order_comment,
                   'products': products,
                   'sender_name': json_data_to_transfer['1']['username']}


        data_send = render_to_string('json_templates/cdek_create_order.txt', context)
        encoded_data = data_send.encode('utf-8')
        # print(encoded_data)

        cdek_json = json.loads(encoded_data)
        print(cdek_json)
        r = requests.post(url, json=cdek_json, headers=headers)

        # r = requests.post(url, json=cdek_json, headers=headers)
        print(r.text)
        return

    print('WAREHOUSE HOHOHO')
    token = register_to_cdec();
    transfer_to_cdec(token=token, data_to_transfer=data_to_transfer);

    return
