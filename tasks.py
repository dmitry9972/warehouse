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

        context = {'user': 'Вася Пупкин'}
        data_send = render_to_string('json_templates/cdek_create_order.txt', context)
        encoded_data = data_send.encode('utf-8')
        print(encoded_data)

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
