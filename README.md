# warehouse

Here my portfolio django-project. It consists of two parts: shop and warehouse.

Shop is an internet shop (only backend on django-rest-framework). Warehouse is aggregator of shops and carriers. 
Shop receives requests with product information for managers and orders from clients. 
Unprocessed orders are being watched by Celery-task, it sends them to warehouse via rest-api.

Warehouse receives orders from shop and sends them to carrier (SDEK). 
Carrier gives response: tracknumber. It is saved to order-record in database. 
After that celery-task sends it back to shop via rest. And tracknumber being saved to shop order-record.


order: client -> shop -> warehouse -> CDEK -> warehouse -> shop


CURL EXAMPLE REQUEST: curl -X POST -H "Authorization: Token 8e58ec44038ab7947bfb07e55f2c6fd2ded2a311" -d "advuser=4&productset=1&productset=1" 'http://localhost:8000/api/order/'



HOW TO INSTALL: 

sudo apt install redis-server  
mkdir shop_warehouse  
cd shop_warehouse  
pip install virtualenv  
virtualenv newenv  
source newenv/bin/activate  
pip install celery==5.1.2  
pip install django_phonenumber_field==5.2.0  
pip install Django==3.2.6  
pip install coloredlogs==15.0.1  
pip install colorlog==6.5.0  
pip install requests==2.26.0  
pip install drf_yasg==1.20.0  
pip install psycopg2_binary==2.9.1  
pip install djangorestframework==3.12.4  
pip install psycopg2==2.9.1  
pip install django-cors-headers  
pip install django-celery-beat==2.2.1  
pip install django-extensions  
pip install phonenumbers=8.12.35  
pip install Pillow==8.4.0  
pip install redis==3.5.3  
  
  
mkdir shop  
cd shop  
git clone http://github.com/dmitry9972/shop.git  
cd ..  
  
mkdir warehouse  
cd warehouse  
git clone http://github.com/dmitry9972/warehouse.git  
  
cd ..   
  
cd shop  
cd shop  
cd epicRUN  
source go.sh  

  

  
Features:  

1)Token-authentication    
2)Swagger  
3)Celery-redis periodic tasks    
4)environment project settings    
5)Custom permision classes (/api/permissions.py)  
6)Router urls.    
7)Tests (api/tests.py)    

    

