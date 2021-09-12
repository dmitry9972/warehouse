from pathlib import Path

SECRET_KEY = 'xxxxxxxx'

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

WAREHOUSE_REDIS_BROKER = 'redis://localhost:xxxx/x'

CDEK_REGISTER_URL = 'https://api.edu.cdek.ru/v2/oauth/token?parameters'

CDEK_ORDERS_URL = 'https://api.edu.cdek.ru/v2/orders'

SHOP_API_TOKEN = 'Token 8e58ec44038ab7947bfb07e55f2c6fd2ded2a311'

SHOP_API_URL = 'http://127.0.0.1:8000/api/order/{}/'

#CDEK EDUCATION LOGIN-PASS
CDEK_LOGIN = 'EMscd6r9JnFiQ3bLoyjJY6eM78JrJceI'
CDEK_PASSWORD = 'PjLZkKBHEiLK3YsjtNrt3TGNG0ahs3kG'
