# warehouse

Here my portfolio django-project. It consists of two parts: shop and warehouse.

Shop is an internet shop (only backend on django-rest-framework). Warehouse is aggregator of shops and carriers. 
Shop receives requests with product information for managers and orders from clients. 
Unprocessed orders are being watched by Celery-task, it sends them to warehouse via rest-api.

Warehouse receives orders from shop and sends them to carrier (SDEK). 
Carrier gives response: tracknumber. It is saved to order-record in database. 
After that celery-task sends it back to shop via rest. And tracknumber being saved to shop order-record.


order: client -> shop -> warehouse -> CDEK -> warehouse -> shop



Features:

1)Token-authentication
2)Swagger
3)Celery-redis periodic tasks
4)Separate project-settings (git-ignored) + settings.example
5)Custom permision classes (/api/permissions.py)
6)Router urls.
7)Tests (api/tests.py)



Requarements:

celery==5.1.2
django_phonenumber_field==5.2.0
Django==3.2.6
coloredlogs==15.0.1
requests==2.26.0
drf_yasg==1.20.0
psycopg2_binary==2.9.1
djangorestframework==3.12.4
psycopg2==2.9.1
