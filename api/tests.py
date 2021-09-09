from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status
from main.models import AdvUser, Order
from rest_framework.authtoken.models import Token
import tasks
from django.db.models import Max
import json
import datetime
from unittest.mock import patch, Mock
from unittest.mock import MagicMock
import requests
from carriers.cdek import CDEK


class ApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.user = AdvUser.objects.create(username='kitty', password='dogedogedoge', email='cat@cats.ru', )
        self.user.is_staff = True
        self.user.set_password('dogedogedoge')
        self.user.save()

    @property
    def token(self):
        url = reverse('login')

        data = {
            'username': 'kitty',
            'password': 'dogedogedoge',
        }

        response = self.client.post(url, data, format='json')

        token = response.json().get('token')
        return token

    def test_account(self):
        url = reverse('register')
        data = {
            'email': 'cat@cats.ru',
            'username': 'catzilla',
            'password': '777777777',
            'password2': '777777777',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AdvUser.objects.count(), 2)

        url = reverse('login')

        data = {
            'username': 'catzilla',
            'password': '777777777',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order(self):
        url = reverse('order')

        response = self.client.get(url, HTTP_AUTHORIZATION='token {}'.format(self.token))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('order-create')
        data = {
            'order_info': "{'1': {'username': 'admin'," +
                          " 'product_name': 'Блинчики с фаршем и салом'," +
                          "'product_count': 3}," +
                          "'2': {'username': 'admin'," +
                          "'product_name': 'Кока-кола'," +
                          "'product_count': 5}}",
            'order_date': '2021-09-02T05:47:51.638063',
            'order_number': 1,
            'order_client': 'admin',
        }

        response = self.client.post(url, data, format='json', HTTP_AUTHORIZATION='token {}'.format(self.token))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)

    def test_cdek(self):
        self.test_order()

        from django.conf import settings
        import os
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "warehouse.settings")
        requests.patch = MagicMock()
        requests.post = MagicMock()

        requests.post.return_value.text=json.dumps({'entity':{'uuid':'123',},
                                                    'access_token':'777'},)


        CDEK_instance = CDEK(settings.CDEK_LOGIN,
                             settings.CDEK_PASSWORD)

        transfer_data = {'order_client': 'cat', 'order_pk': 1, 'order_date': '2021-09-17T10:33:13.628274Z',
                         'order_info': '{"1": {"username": "admin", "product_name": "Блинчики с фаршем и салом", "product_count": 3}, "2": {"username": "admin", "product_name": "Кока-кола", "product_count": 5}}'}
        order_pk = 1
        CDEK_instance.send_order_to_cdec(transfer_data, order_pk)

        self.assertEqual(requests.post.called, True)
        self.assertEqual(requests.patch.called, True)
